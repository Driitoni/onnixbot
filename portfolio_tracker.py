"""
Portfolio Tracker Module for Pocket Option Trading Bot
Tracks trading performance, win rates, and portfolio metrics
"""

import json
import os
from datetime import datetime, timedelta
from typing import Dict, List, Optional, Tuple
import logging
import pandas as pd
from dataclasses import dataclass, asdict
from enum import Enum

logger = logging.getLogger(__name__)

class TradeStatus(Enum):
    """Trade status enumeration"""
    OPEN = "open"
    CLOSED_WIN = "closed_win"
    CLOSED_LOSS = "closed_loss"
    CLOSED_BREAKEVEN = "closed_breakeven"

class TradeType(Enum):
    """Trade type enumeration"""
    BUY = "buy"
    SELL = "sell"

@dataclass
class Trade:
    """Trade data class"""
    id: str
    symbol: str
    trade_type: TradeType
    entry_price: float
    exit_price: Optional[float]
    quantity: float
    entry_time: datetime
    exit_time: Optional[datetime]
    status: TradeStatus
    stop_loss: Optional[float]
    take_profit: Optional[float]
    profit_loss: Optional[float]
    confidence: int
    signal_reasons: List[str]
    timeframe: str
    
    def to_dict(self) -> Dict:
        """Convert trade to dictionary"""
        return asdict(self)
    
    @classmethod
    def from_dict(cls, data: Dict) -> 'Trade':
        """Create trade from dictionary"""
        # Convert datetime strings back to datetime objects
        if isinstance(data['entry_time'], str):
            data['entry_time'] = datetime.fromisoformat(data['entry_time'])
        if data['exit_time'] and isinstance(data['exit_time'], str):
            data['exit_time'] = datetime.fromisoformat(data['exit_time'])
        
        # Convert enums
        data['trade_type'] = TradeType(data['trade_type'])
        data['status'] = TradeStatus(data['status'])
        
        return cls(**data)

class PortfolioTracker:
    """Advanced portfolio tracking system"""
    
    def __init__(self, data_file: str = "portfolio_data.json"):
        self.data_file = data_file
        self.trades: List[Trade] = []
        self.daily_stats = {}
        self.load_data()
    
    def load_data(self):
        """Load portfolio data from file"""
        try:
            if os.path.exists(self.data_file):
                with open(self.data_file, 'r') as f:
                    data = json.load(f)
                    self.trades = [Trade.from_dict(trade_data) for trade_data in data.get('trades', [])]
                    self.daily_stats = data.get('daily_stats', {})
                logger.info(f"Loaded {len(self.trades)} trades from {self.data_file}")
            else:
                logger.info("No existing portfolio data found, starting fresh")
        except Exception as e:
            logger.error(f"Error loading portfolio data: {e}")
            self.trades = []
            self.daily_stats = {}
    
    def save_data(self):
        """Save portfolio data to file"""
        try:
            data = {
                'trades': [trade.to_dict() for trade in self.trades],
                'daily_stats': self.daily_stats,
                'last_updated': datetime.now().isoformat()
            }
            
            # Convert datetime objects to strings for JSON serialization
            for trade_dict in data['trades']:
                trade_dict['entry_time'] = trade_dict['entry_time'].isoformat()
                if trade_dict['exit_time']:
                    trade_dict['exit_time'] = trade_dict['exit_time'].isoformat()
            
            with open(self.data_file, 'w') as f:
                json.dump(data, f, indent=2)
            
            logger.info(f"Portfolio data saved to {self.data_file}")
        except Exception as e:
            logger.error(f"Error saving portfolio data: {e}")
    
    def add_trade(self, trade: Trade):
        """Add a new trade to the portfolio"""
        self.trades.append(trade)
        self.update_daily_stats()
        self.save_data()
        logger.info(f"Added trade: {trade.symbol} {trade.trade_type.value} at {trade.entry_price}")
    
    def close_trade(self, trade_id: str, exit_price: float, exit_time: Optional[datetime] = None) -> bool:
        """Close an existing trade"""
        if exit_time is None:
            exit_time = datetime.now()
        
        for trade in self.trades:
            if trade.id == trade_id and trade.status == TradeStatus.OPEN:
                trade.exit_price = exit_price
                trade.exit_time = exit_time
                trade.status = TradeStatus.CLOSED_WIN if exit_price > trade.entry_price else TradeStatus.CLOSED_LOSS
                
                # Calculate profit/loss
                if trade.trade_type == TradeType.BUY:
                    trade.profit_loss = (exit_price - trade.entry_price) * trade.quantity
                else:
                    trade.profit_loss = (trade.entry_price - exit_price) * trade.quantity
                
                self.update_daily_stats()
                self.save_data()
                logger.info(f"Closed trade {trade_id}: P&L = ${trade.profit_loss:.2f}")
                return True
        
        logger.warning(f"Trade {trade_id} not found or already closed")
        return False
    
    def get_open_trades(self) -> List[Trade]:
        """Get all open trades"""
        return [trade for trade in self.trades if trade.status == TradeStatus.OPEN]
    
    def get_closed_trades(self, days: int = 30) -> List[Trade]:
        """Get closed trades within specified days"""
        cutoff_date = datetime.now() - timedelta(days=days)
        return [
            trade for trade in self.trades 
            if trade.status != TradeStatus.OPEN and trade.exit_time and trade.exit_time >= cutoff_date
        ]
    
    def get_trade_statistics(self, days: int = 30) -> Dict:
        """Calculate comprehensive trade statistics"""
        closed_trades = self.get_closed_trades(days)
        
        if not closed_trades:
            return {
                'total_trades': 0,
                'win_rate': 0,
                'total_profit_loss': 0,
                'avg_win': 0,
                'avg_loss': 0,
                'largest_win': 0,
                'largest_loss': 0,
                'profit_factor': 0,
                'avg_trade_duration': 0
            }
        
        winning_trades = [t for t in closed_trades if t.profit_loss and t.profit_loss > 0]
        losing_trades = [t for t in closed_trades if t.profit_loss and t.profit_loss < 0]
        
        total_profit = sum(t.profit_loss for t in winning_trades if t.profit_loss) or 0
        total_loss = sum(t.profit_loss for t in losing_trades if t.profit_loss) or 0
        
        win_rate = (len(winning_trades) / len(closed_trades)) * 100 if closed_trades else 0
        avg_win = total_profit / len(winning_trades) if winning_trades else 0
        avg_loss = total_loss / len(losing_trades) if losing_trades else 0
        largest_win = max((t.profit_loss for t in winning_trades if t.profit_loss), default=0)
        largest_loss = min((t.profit_loss for t in losing_trades if t.profit_loss), default=0)
        
        profit_factor = abs(total_profit / total_loss) if total_loss != 0 else float('inf') if total_profit > 0 else 0
        
        # Calculate average trade duration
        durations = []
        for trade in closed_trades:
            if trade.exit_time and trade.exit_time != trade.entry_time:
                duration = (trade.exit_time - trade.entry_time).total_seconds() / 3600  # in hours
                durations.append(duration)
        
        avg_duration = sum(durations) / len(durations) if durations else 0
        
        return {
            'total_trades': len(closed_trades),
            'winning_trades': len(winning_trades),
            'losing_trades': len(losing_trades),
            'win_rate': round(win_rate, 2),
            'total_profit_loss': round(total_profit + total_loss, 2),
            'total_profit': round(total_profit, 2),
            'total_loss': round(total_loss, 2),
            'avg_win': round(avg_win, 2),
            'avg_loss': round(avg_loss, 2),
            'largest_win': round(largest_win, 2),
            'largest_loss': round(largest_loss, 2),
            'profit_factor': round(profit_factor, 2),
            'avg_trade_duration': round(avg_duration, 2),
            'consecutive_wins': self._get_consecutive_wins(),
            'consecutive_losses': self._get_consecutive_losses()
        }
    
    def _get_consecutive_wins(self) -> int:
        """Get current consecutive wins streak"""
        consecutive = 0
        for trade in reversed(self.trades):
            if trade.status == TradeStatus.CLOSED_WIN and trade.profit_loss and trade.profit_loss > 0:
                consecutive += 1
            elif trade.status in [TradeStatus.CLOSED_LOSS, TradeStatus.CLOSED_BREAKEVEN]:
                break
        return consecutive
    
    def _get_consecutive_losses(self) -> int:
        """Get current consecutive losses streak"""
        consecutive = 0
        for trade in reversed(self.trades):
            if trade.status == TradeStatus.CLOSED_LOSS and trade.profit_loss and trade.profit_loss < 0:
                consecutive += 1
            elif trade.status in [TradeStatus.CLOSED_WIN, TradeStatus.CLOSED_BREAKEVEN]:
                break
        return consecutive
    
    def get_symbol_performance(self, symbol: str, days: int = 30) -> Dict:
        """Get performance statistics for a specific symbol"""
        symbol_trades = [
            trade for trade in self.get_closed_trades(days)
            if trade.symbol == symbol
        ]
        
        if not symbol_trades:
            return {
                'symbol': symbol,
                'total_trades': 0,
                'win_rate': 0,
                'profit_loss': 0
            }
        
        winning_trades = [t for t in symbol_trades if t.profit_loss and t.profit_loss > 0]
        win_rate = (len(winning_trades) / len(symbol_trades)) * 100
        total_pnl = sum(t.profit_loss for t in symbol_trades if t.profit_loss) or 0
        
        return {
            'symbol': symbol,
            'total_trades': len(symbol_trades),
            'winning_trades': len(winning_trades),
            'win_rate': round(win_rate, 2),
            'profit_loss': round(total_pnl, 2),
            'avg_trade_pnl': round(total_pnl / len(symbol_trades), 2) if symbol_trades else 0
        }
    
    def get_timeframe_performance(self, timeframe: str, days: int = 30) -> Dict:
        """Get performance statistics for a specific timeframe"""
        tf_trades = [
            trade for trade in self.get_closed_trades(days)
            if trade.timeframe == timeframe
        ]
        
        if not tf_trades:
            return {
                'timeframe': timeframe,
                'total_trades': 0,
                'win_rate': 0,
                'profit_loss': 0
            }
        
        winning_trades = [t for t in tf_trades if t.profit_loss and t.profit_loss > 0]
        win_rate = (len(winning_trades) / len(tf_trades)) * 100
        total_pnl = sum(t.profit_loss for t in tf_trades if t.profit_loss) or 0
        
        return {
            'timeframe': timeframe,
            'total_trades': len(tf_trades),
            'winning_trades': len(winning_trades),
            'win_rate': round(win_rate, 2),
            'profit_loss': round(total_pnl, 2),
            'avg_trade_pnl': round(total_pnl / len(tf_trades), 2) if tf_trades else 0
        }
    
    def get_daily_performance(self, date: Optional[datetime] = None) -> Dict:
        """Get daily performance for a specific date"""
        if date is None:
            date = datetime.now()
        
        date_str = date.strftime('%Y-%m-%d')
        daily_trades = [
            trade for trade in self.trades
            if trade.entry_time.strftime('%Y-%m-%d') == date_str
        ]
        
        if not daily_trades:
            return {
                'date': date_str,
                'total_trades': 0,
                'closed_trades': 0,
                'profit_loss': 0,
                'win_rate': 0
            }
        
        closed_daily = [t for t in daily_trades if t.status != TradeStatus.OPEN]
        winning_daily = [t for t in closed_daily if t.profit_loss and t.profit_loss > 0]
        
        win_rate = (len(winning_daily) / len(closed_daily)) * 100 if closed_daily else 0
        total_pnl = sum(t.profit_loss for t in closed_daily if t.profit_loss) or 0
        
        return {
            'date': date_str,
            'total_trades': len(daily_trades),
            'closed_trades': len(closed_daily),
            'open_trades': len(daily_trades) - len(closed_daily),
            'winning_trades': len(winning_daily),
            'losing_trades': len(closed_daily) - len(winning_daily),
            'win_rate': round(win_rate, 2),
            'profit_loss': round(total_pnl, 2)
        }
    
    def update_daily_stats(self):
        """Update daily statistics"""
        today = datetime.now().strftime('%Y-%m-%d')
        today_performance = self.get_daily_performance()
        
        self.daily_stats[today] = today_performance
        
        # Keep only last 30 days of daily stats
        cutoff_date = (datetime.now() - timedelta(days=30)).strftime('%Y-%m-%d')
        self.daily_stats = {
            date: stats for date, stats in self.daily_stats.items()
            if date >= cutoff_date
        }
    
    def get_summary(self) -> Dict:
        """Get portfolio summary"""
        total_stats = self.get_trade_statistics(30)
        open_trades = self.get_open_trades()
        today_stats = self.get_daily_performance()
        
        return {
            'total_trades': total_stats['total_trades'],
            'open_trades': len(open_trades),
            'win_rate': total_stats['win_rate'],
            'total_profit_loss': total_stats['total_profit_loss'],
            'today_pnl': today_stats['profit_loss'],
            'consecutive_wins': total_stats['consecutive_wins'],
            'consecutive_losses': total_stats['consecutive_losses'],
            'largest_win': total_stats['largest_win'],
            'largest_loss': total_stats['largest_loss'],
            'profit_factor': total_stats['profit_factor']
        }
    
    def generate_performance_report(self, days: int = 30) -> str:
        """Generate detailed performance report"""
        stats = self.get_trade_statistics(days)
        
        report = f"""
📊 **Performance Report (Last {days} Days)**

**📈 Overall Statistics:**
• Total Trades: {stats['total_trades']}
• Win Rate: {stats['win_rate']}%
• Total P&L: ${stats['total_profit_loss']}
• Profit Factor: {stats['profit_factor']}

**🎯 Trade Analysis:**
• Winning Trades: {stats['winning_trades']}
• Losing Trades: {stats['losing_trades']}
• Average Win: ${stats['avg_win']}
• Average Loss: ${stats['avg_loss']}
• Largest Win: ${stats['largest_win']}
• Largest Loss: ${stats['largest_loss']}

**📅 Streaks:**
• Consecutive Wins: {stats['consecutive_wins']}
• Consecutive Losses: {stats['consecutive_losses']}
• Average Duration: {stats['avg_trade_duration']:.1f} hours
        """
        
        return report
    
    def export_trades_to_csv(self, filename: str = "trades_export.csv"):
        """Export trades to CSV file"""
        try:
            if not self.trades:
                logger.warning("No trades to export")
                return
            
            # Convert trades to DataFrame
            trade_data = []
            for trade in self.trades:
                trade_data.append({
                    'ID': trade.id,
                    'Symbol': trade.symbol,
                    'Type': trade.trade_type.value,
                    'Entry Price': trade.entry_price,
                    'Exit Price': trade.exit_price or '',
                    'Quantity': trade.quantity,
                    'Entry Time': trade.entry_time,
                    'Exit Time': trade.exit_time or '',
                    'Status': trade.status.value,
                    'Stop Loss': trade.stop_loss or '',
                    'Take Profit': trade.take_profit or '',
                    'Profit/Loss': trade.profit_loss or '',
                    'Confidence': trade.confidence,
                    'Timeframe': trade.timeframe,
                    'Signal Reasons': '; '.join(trade.signal_reasons)
                })
            
            df = pd.DataFrame(trade_data)
            df.to_csv(filename, index=False)
            logger.info(f"Trades exported to {filename}")
            
        except Exception as e:
            logger.error(f"Error exporting trades to CSV: {e}")
    
    def get_risk_metrics(self) -> Dict:
        """Calculate portfolio risk metrics"""
        closed_trades = self.get_closed_trades(30)
        
        if not closed_trades:
            return {
                'max_drawdown': 0,
                'var_95': 0,
                'sharpe_ratio': 0,
                'max_consecutive_losses': 0
            }
        
        # Calculate returns
        returns = [t.profit_loss for t in closed_trades if t.profit_loss]
        
        if not returns:
            return {
                'max_drawdown': 0,
                'var_95': 0,
                'sharpe_ratio': 0,
                'max_consecutive_losses': 0
            }
        
        # Value at Risk (95% confidence)
        var_95 = sorted(returns)[int(len(returns) * 0.05)]
        
        # Maximum consecutive losses
        max_consecutive_losses = 0
        current_consecutive = 0
        for trade in reversed(closed_trades):
            if trade.profit_loss and trade.profit_loss < 0:
                current_consecutive += 1
                max_consecutive_losses = max(max_consecutive_losses, current_consecutive)
            else:
                current_consecutive = 0
        
        # Simplified Sharpe ratio calculation
        avg_return = sum(returns) / len(returns)
        return_std = pd.Series(returns).std() if len(returns) > 1 else 0
        sharpe_ratio = avg_return / return_std if return_std > 0 else 0
        
        # Maximum drawdown (simplified)
        max_drawdown = min(returns) if returns else 0
        
        return {
            'max_drawdown': round(max_drawdown, 2),
            'var_95': round(var_95, 2),
            'sharpe_ratio': round(sharpe_ratio, 2),
            'max_consecutive_losses': max_consecutive_losses
        }