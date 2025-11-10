"""
Risk Management Module for Pocket Option Trading Bot
Implements comprehensive risk management and position sizing
"""

import pandas as pd
import numpy as np
from typing import Dict, List, Optional
import logging
from datetime import datetime, timedelta
import json
import os

class RiskManager:
    """Advanced risk management system for trading"""
    
    def __init__(self, config: Dict):
        self.config = config
        self.logger = logging.getLogger(__name__)
        self.daily_stats = {
            'trades_taken': 0,
            'signals_sent': 0,
            'max_trades_reached': False,
            'win_rate': 0.0,
            'profit_loss': 0.0,
            'last_reset': datetime.now().date()
        }
        
    def calculate_position_size(self, account_balance: float, risk_percentage: float, 
                              stop_loss_distance: float) -> float:
        """Calculate position size based on risk management rules"""
        risk_amount = account_balance * (risk_percentage / 100)
        position_size = risk_amount / stop_loss_distance if stop_loss_distance > 0 else 0
        
        # Apply maximum position size limit
        max_position = self.config.get('MAX_POSITION_SIZE', 100)
        return min(position_size, max_position)
    
    def assess_trade_risk(self, signal: Dict, account_balance: float = 1000) -> Dict:
        """Comprehensive risk assessment for a trading signal"""
        risk_assessment = {
            'risk_level': 'LOW',
            'score': 0,
            'max_loss': 0,
            'risk_reward_ratio': 0,
            'warnings': [],
            'recommendation': 'APPROVED',
            'position_size': 0
        }
        
        try:
            current_price = signal.get('current_price', 0)
            stop_loss = signal.get('stop_loss', 0)
            take_profit = signal.get('take_profit', 0)
            confidence = signal.get('confidence', 0)
            
            if current_price == 0 or stop_loss == 0:
                risk_assessment['recommendation'] = 'REJECTED'
                risk_assessment['warnings'].append('Invalid price data')
                return risk_assessment
            
            # Calculate stop loss distance
            stop_distance = abs(current_price - stop_loss)
            risk_percent = (stop_distance / current_price) * 100
            
            # Calculate risk-reward ratio
            if signal.get('signal') == 'BUY':
                profit_distance = take_profit - current_price
            else:
                profit_distance = current_price - take_profit
            
            if stop_distance > 0:
                risk_reward_ratio = profit_distance / stop_distance
            else:
                risk_reward_ratio = 0
            
            risk_assessment['risk_reward_ratio'] = risk_reward_ratio
            risk_assessment['max_loss'] = stop_distance
            
            # Risk scoring system
            risk_score = 0
            
            # 1. Risk-reward ratio assessment
            if risk_reward_ratio < 1:
                risk_score += 3
                risk_assessment['warnings'].append('Poor risk-reward ratio')
            elif risk_reward_ratio < 1.5:
                risk_score += 1
            else:
                risk_score -= 1  # Good risk-reward
            
            # 2. Stop loss distance assessment
            if risk_percent > 5:
                risk_score += 2
                risk_assessment['warnings'].append('High stop loss percentage')
            elif risk_percent < 1:
                risk_score += 1
                risk_assessment['warnings'].append('Very tight stop loss')
            
            # 3. Confidence level assessment
            if confidence < 30:
                risk_score += 2
                risk_assessment['warnings'].append('Low signal confidence')
            elif confidence > 70:
                risk_score -= 2  # High confidence
            
            # 4. Technical indicator alignment
            indicators = signal.get('technical_indicators', {})
            alignment_score = 0
            
            # RSI check
            rsi = indicators.get('RSI', 50)
            if (signal.get('signal') == 'BUY' and 30 < rsi < 70) or \
               (signal.get('signal') == 'SELL' and 30 < rsi < 70):
                alignment_score += 1
            else:
                alignment_score -= 1
            
            # MACD check
            macd = indicators.get('MACD', 0)
            macd_signal = indicators.get('MACD_Signal', 0)
            if (signal.get('signal') == 'BUY' and macd > macd_signal) or \
               (signal.get('signal') == 'SELL' and macd < macd_signal):
                alignment_score += 1
            else:
                alignment_score -= 1
            
            risk_score += alignment_score
            
            # 5. Market volatility check
            adx = indicators.get('ADX', 0)
            if adx > 30:
                risk_score += 1  # High volatility increases risk
                risk_assessment['warnings'].append('High market volatility')
            
            risk_assessment['score'] = risk_score
            
            # Determine risk level
            if risk_score <= -2:
                risk_assessment['risk_level'] = 'VERY_LOW'
            elif risk_score <= 0:
                risk_assessment['risk_level'] = 'LOW'
            elif risk_score <= 2:
                risk_assessment['risk_level'] = 'MEDIUM'
            elif risk_score <= 4:
                risk_assessment['risk_level'] = 'HIGH'
            else:
                risk_assessment['risk_level'] = 'VERY_HIGH'
            
            # Calculate recommended position size
            position_size = self.calculate_position_size(
                account_balance, 
                self.config.get('RISK_PERCENTAGE', 2.0), 
                stop_distance
            )
            risk_assessment['position_size'] = position_size
            
            # Final recommendation
            if risk_score > 4 or confidence < 20:
                risk_assessment['recommendation'] = 'REJECTED'
            elif risk_score > 2:
                risk_assessment['recommendation'] = 'CAUTION'
            
            # Daily limits check
            if self.check_daily_limits():
                risk_assessment['recommendation'] = 'REJECTED'
                risk_assessment['warnings'].append('Daily trading limit reached')
            
        except Exception as e:
            self.logger.error(f"Error in risk assessment: {e}")
            risk_assessment['recommendation'] = 'ERROR'
            risk_assessment['warnings'].append(f'Risk assessment error: {str(e)}')
        
        return risk_assessment
    
    def check_daily_limits(self) -> bool:
        """Check if daily trading limits are reached"""
        current_date = datetime.now().date()
        
        # Reset daily stats if it's a new day
        if self.daily_stats['last_reset'] != current_date:
            self.reset_daily_stats()
        
        max_signals = self.config.get('MAX_DAILY_SIGNALS', 50)
        return self.daily_stats['signals_sent'] >= max_signals
    
    def reset_daily_stats(self):
        """Reset daily trading statistics"""
        self.daily_stats = {
            'trades_taken': 0,
            'signals_sent': 0,
            'max_trades_reached': False,
            'win_rate': 0.0,
            'profit_loss': 0.0,
            'last_reset': datetime.now().date()
        }
        self.logger.info("Daily stats reset")
    
    def update_daily_stats(self, signal_sent: bool = False, trade_result: Optional[Dict] = None):
        """Update daily trading statistics"""
        current_date = datetime.now().date()
        
        if self.daily_stats['last_reset'] != current_date:
            self.reset_daily_stats()
        
        if signal_sent:
            self.daily_stats['signals_sent'] += 1
        
        if trade_result:
            self.daily_stats['trades_taken'] += 1
            if 'profit_loss' in trade_result:
                self.daily_stats['profit_loss'] += trade_result['profit_loss']
    
    def get_daily_summary(self) -> Dict:
        """Get daily trading summary"""
        return {
            'date': datetime.now().date().strftime('%Y-%m-%d'),
            'signals_sent': self.daily_stats['signals_sent'],
            'trades_taken': self.daily_stats['trades_taken'],
            'profit_loss': round(self.daily_stats['profit_loss'], 2),
            'remaining_signals': max(0, self.config.get('MAX_DAILY_SIGNALS', 50) - self.daily_stats['signals_sent']),
            'max_trades_reached': self.daily_stats['signals_sent'] >= self.config.get('MAX_DAILY_SIGNALS', 50)
        }
    
    def calculate_drawdown_risk(self, account_balance: float, current_drawdown: float) -> Dict:
        """Calculate drawdown risk metrics"""
        max_drawdown_limit = self.config.get('MAX_DRAWDOWN_PERCENTAGE', 10)
        current_drawdown_pct = (current_drawdown / account_balance) * 100
        
        drawdown_risk = {
            'current_drawdown_pct': round(current_drawdown_pct, 2),
            'max_drawdown_limit': max_drawdown_limit,
            'risk_level': 'LOW',
            'action_required': False
        }
        
        if current_drawdown_pct >= max_drawdown_limit * 0.8:
            drawdown_risk['risk_level'] = 'HIGH'
            drawdown_risk['action_required'] = True
            drawdown_risk['message'] = 'Approaching maximum drawdown limit'
        elif current_drawdown_pct >= max_drawdown_limit * 0.5:
            drawdown_risk['risk_level'] = 'MEDIUM'
            drawdown_risk['message'] = 'Moderate drawdown detected'
        
        return drawdown_risk
    
    def portfolio_heat_check(self, current_positions: List[Dict], account_balance: float) -> Dict:
        """Check overall portfolio heat (total exposure)"""
        total_exposure = sum(pos.get('size', 0) for pos in current_positions)
        max_portfolio_heat = self.config.get('MAX_PORTFOLIO_HEAT', 20)  # 20% of account
        
        portfolio_heat_pct = (total_exposure / account_balance) * 100 if account_balance > 0 else 0
        
        heat_check = {
            'total_exposure': total_exposure,
            'portfolio_heat_pct': round(portfolio_heat_pct, 2),
            'max_allowed_heat_pct': max_portfolio_heat,
            'status': 'SAFE',
            'warnings': []
        }
        
        if portfolio_heat_pct > max_portfolio_heat:
            heat_check['status'] = 'DANGEROUS'
            heat_check['warnings'].append('Portfolio heat exceeds safe limits')
        elif portfolio_heat_pct > max_portfolio_heat * 0.8:
            heat_check['status'] = 'CAUTION'
            heat_check['warnings'].append('High portfolio exposure')
        
        return heat_check
    
    def generate_risk_report(self, signals: List[Dict], account_balance: float = 1000) -> Dict:
        """Generate comprehensive risk report for multiple signals"""
        if not signals:
            return {'error': 'No signals provided'}
        
        report = {
            'timestamp': datetime.now().strftime('%Y-%m-%d %H:%M:%S'),
            'signals_analyzed': len(signals),
            'account_balance': account_balance,
            'individual_assessments': [],
            'portfolio_overview': {
                'total_risk_score': 0,
                'average_confidence': 0,
                'high_risk_count': 0,
                'approved_signals': [],
                'rejected_signals': []
            },
            'recommendations': []
        }
        
        total_risk_score = 0
        total_confidence = 0
        approved_count = 0
        
        for signal in signals:
            assessment = self.assess_trade_risk(signal, account_balance)
            report['individual_assessments'].append({
                'symbol': signal.get('symbol'),
                'signal': signal.get('signal'),
                'risk_level': assessment['risk_level'],
                'recommendation': assessment['recommendation'],
                'position_size': assessment['position_size'],
                'warnings': assessment['warnings']
            })
            
            if assessment['recommendation'] == 'APPROVED':
                approved_count += 1
                report['portfolio_overview']['approved_signals'].append(signal.get('symbol'))
            else:
                report['portfolio_overview']['rejected_signals'].append(signal.get('symbol'))
            
            # Convert risk level to score for aggregation
            risk_score_map = {
                'VERY_LOW': -2, 'LOW': -1, 'MEDIUM': 0, 
                'HIGH': 1, 'VERY_HIGH': 2
            }
            total_risk_score += risk_score_map.get(assessment['risk_level'], 0)
            total_confidence += signal.get('confidence', 0)
            
            if assessment['risk_level'] in ['HIGH', 'VERY_HIGH']:
                report['portfolio_overview']['high_risk_count'] += 1
        
        # Calculate portfolio metrics
        report['portfolio_overview']['total_risk_score'] = total_risk_score
        report['portfolio_overview']['average_confidence'] = total_confidence / len(signals) if signals else 0
        
        # Generate recommendations
        if approved_count == 0:
            report['recommendations'].append("No signals meet risk criteria - Consider widening parameters or wait for better setups")
        elif approved_count > 5:
            report['recommendations'].append("High number of approved signals - Consider reducing position sizes")
        
        if report['portfolio_overview']['high_risk_count'] > 0:
            report['recommendations'].append("High-risk signals detected - Review market conditions before proceeding")
        
        # Overall portfolio risk assessment
        if total_risk_score > 3:
            report['overall_risk'] = 'HIGH'
        elif total_risk_score > 1:
            report['overall_risk'] = 'MEDIUM'
        else:
            report['overall_risk'] = 'LOW'
        
        return report