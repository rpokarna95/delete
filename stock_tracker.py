#!/usr/bin/env python3
"""
Stock Performance Tracker
A treasure map to analyze if yer stocks be sailin' smooth or sinkin' to the depths!
"""

import sys
from datetime import datetime, timedelta
from typing import Optional, Tuple

try:
    import yfinance as yf
except ImportError:
    print("Ahoy! Ye need to install yfinance first, matey!")
    print("Run: pip install yfinance")
    sys.exit(1)


class StockTracker:
    """A class to track and analyze stock performance."""

    def __init__(self, ticker: str):
        """
        Initialize the stock tracker with a ticker symbol.
        
        Args:
            ticker: The stock ticker symbol (e.g., 'AAPL', 'GOOGL')
        """
        self.ticker = ticker.upper().strip()
        self.stock = None
        self.current_price = None
        self.historical_data = None

    def fetch_stock_data(self) -> bool:
        """
        Fetch current and historical stock data.
        
        Returns:
            True if data was fetched successfully, False otherwise.
        """
        try:
            self.stock = yf.Ticker(self.ticker)
            
            # Fetch historical data for the past year
            end_date = datetime.now()
            start_date = end_date - timedelta(days=365)
            
            self.historical_data = self.stock.history(
                start=start_date.strftime('%Y-%m-%d'),
                end=end_date.strftime('%Y-%m-%d')
            )
            
            if self.historical_data.empty:
                return False
            
            # Get the most recent closing price
            self.current_price = self.historical_data['Close'].iloc[-1]
            
            return True
            
        except Exception as e:
            print(f"Error fetchin' data for {self.ticker}: {e}")
            return False

    def calculate_metrics(self) -> Optional[dict]:
        """
        Calculate performance metrics for the stock.
        
        Returns:
            Dictionary containing performance metrics or None if data is unavailable.
        """
        if self.historical_data is None or self.historical_data.empty:
            return None
        
        close_prices = self.historical_data['Close']
        
        # Calculate various averages
        avg_50_day = close_prices.tail(50).mean() if len(close_prices) >= 50 else close_prices.mean()
        avg_200_day = close_prices.tail(200).mean() if len(close_prices) >= 200 else close_prices.mean()
        overall_avg = close_prices.mean()
        
        # Calculate price changes
        price_52_week_high = close_prices.max()
        price_52_week_low = close_prices.min()
        
        # Calculate percentage changes
        if len(close_prices) >= 2:
            first_price = close_prices.iloc[0]
            yearly_change_pct = ((self.current_price - first_price) / first_price) * 100
        else:
            yearly_change_pct = 0.0
        
        # Calculate recent trend (last 30 days)
        if len(close_prices) >= 30:
            price_30_days_ago = close_prices.iloc[-30]
            monthly_change_pct = ((self.current_price - price_30_days_ago) / price_30_days_ago) * 100
        else:
            monthly_change_pct = 0.0
        
        # Calculate weekly trend
        if len(close_prices) >= 5:
            price_5_days_ago = close_prices.iloc[-5]
            weekly_change_pct = ((self.current_price - price_5_days_ago) / price_5_days_ago) * 100
        else:
            weekly_change_pct = 0.0
        
        return {
            'current_price': self.current_price,
            'avg_50_day': avg_50_day,
            'avg_200_day': avg_200_day,
            'overall_avg': overall_avg,
            'price_52_week_high': price_52_week_high,
            'price_52_week_low': price_52_week_low,
            'yearly_change_pct': yearly_change_pct,
            'monthly_change_pct': monthly_change_pct,
            'weekly_change_pct': weekly_change_pct,
            'data_points': len(close_prices)
        }

    def analyze_performance(self, metrics: dict) -> Tuple[str, list]:
        """
        Analyze stock performance based on calculated metrics.
        
        Args:
            metrics: Dictionary containing performance metrics.
            
        Returns:
            Tuple of (overall_status, list_of_reasons)
        """
        positive_signals = []
        negative_signals = []
        
        # Check if price is above/below moving averages
        if metrics['current_price'] > metrics['avg_50_day']:
            positive_signals.append("Price be above the 50-day average (bullish signal)")
        else:
            negative_signals.append("Price be below the 50-day average (bearish signal)")
        
        if metrics['current_price'] > metrics['avg_200_day']:
            positive_signals.append("Price be above the 200-day average (long-term bullish)")
        else:
            negative_signals.append("Price be below the 200-day average (long-term bearish)")
        
        # Check recent trends
        if metrics['weekly_change_pct'] > 0:
            positive_signals.append(f"Weekly trend be positive (+{metrics['weekly_change_pct']:.2f}%)")
        else:
            negative_signals.append(f"Weekly trend be negative ({metrics['weekly_change_pct']:.2f}%)")
        
        if metrics['monthly_change_pct'] > 0:
            positive_signals.append(f"Monthly trend be positive (+{metrics['monthly_change_pct']:.2f}%)")
        else:
            negative_signals.append(f"Monthly trend be negative ({metrics['monthly_change_pct']:.2f}%)")
        
        if metrics['yearly_change_pct'] > 0:
            positive_signals.append(f"Yearly performance be positive (+{metrics['yearly_change_pct']:.2f}%)")
        else:
            negative_signals.append(f"Yearly performance be negative ({metrics['yearly_change_pct']:.2f}%)")
        
        # Check position relative to 52-week range
        price_range = metrics['price_52_week_high'] - metrics['price_52_week_low']
        if price_range > 0:
            position_pct = ((metrics['current_price'] - metrics['price_52_week_low']) / price_range) * 100
            if position_pct >= 70:
                positive_signals.append(f"Trading near 52-week high (top {100-position_pct:.1f}% of range)")
            elif position_pct <= 30:
                negative_signals.append(f"Trading near 52-week low (bottom {position_pct:.1f}% of range)")
        
        # Determine overall status
        if len(positive_signals) > len(negative_signals):
            overall_status = "DOING GOOD"
            reasons = positive_signals
        elif len(negative_signals) > len(positive_signals):
            overall_status = "DOING BAD"
            reasons = negative_signals
        else:
            overall_status = "MIXED"
            reasons = positive_signals + negative_signals
        
        return overall_status, reasons

    def display_results(self, metrics: dict, status: str, reasons: list) -> None:
        """
        Display the analysis results in a clear, readable format.
        
        Args:
            metrics: Dictionary containing performance metrics.
            status: Overall performance status.
            reasons: List of reasons supporting the status.
        """
        print("\n" + "=" * 60)
        print(f"  STOCK PERFORMANCE REPORT FOR: {self.ticker}")
        print("=" * 60)
        
        print(f"\n  Current Price: ${metrics['current_price']:.2f}")
        print("-" * 60)
        
        print("\n  PRICE AVERAGES:")
        print(f"    50-Day Average:  ${metrics['avg_50_day']:.2f}")
        print(f"    200-Day Average: ${metrics['avg_200_day']:.2f}")
        print(f"    Overall Average: ${metrics['overall_avg']:.2f}")
        
        print("\n  52-WEEK RANGE:")
        print(f"    High: ${metrics['price_52_week_high']:.2f}")
        print(f"    Low:  ${metrics['price_52_week_low']:.2f}")
        
        print("\n  PERFORMANCE TRENDS:")
        print(f"    Weekly Change:  {metrics['weekly_change_pct']:+.2f}%")
        print(f"    Monthly Change: {metrics['monthly_change_pct']:+.2f}%")
        print(f"    Yearly Change:  {metrics['yearly_change_pct']:+.2f}%")
        
        print("\n" + "-" * 60)
        print(f"\n  OVERALL VERDICT: *** {status} ***")
        print("\n  ANALYSIS:")
        for i, reason in enumerate(reasons, 1):
            print(f"    {i}. {reason}")
        
        print("\n" + "=" * 60)
        print(f"  Data based on {metrics['data_points']} trading days")
        print("=" * 60 + "\n")


def validate_ticker(ticker: str) -> bool:
    """
    Validate that the ticker symbol is in a reasonable format.
    
    Args:
        ticker: The stock ticker symbol to validate.
        
    Returns:
        True if the ticker format is valid, False otherwise.
    """
    if not ticker:
        return False
    
    ticker = ticker.strip()
    
    # Ticker should be 1-5 characters and alphanumeric (with possible dots for some tickers)
    if len(ticker) < 1 or len(ticker) > 10:
        return False
    
    # Allow alphanumeric and dots/dashes (for tickers like BRK.B or BRK-B)
    valid_chars = set('ABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789.-')
    return all(char.upper() in valid_chars for char in ticker)


def main():
    """Main function to run the stock tracker."""
    print("\n" + "~" * 60)
    print("  Welcome aboard the STOCK PERFORMANCE TRACKER!")
    print("  Set sail to discover if yer stocks be treasures or trash!")
    print("~" * 60)
    
    while True:
        print("\nEnter a stock ticker symbol (or 'quit' to abandon ship): ", end="")
        
        try:
            ticker_input = input().strip()
        except (EOFError, KeyboardInterrupt):
            print("\n\nFare thee well, matey! May yer portfolios always prosper!")
            break
        
        if ticker_input.lower() in ('quit', 'exit', 'q'):
            print("\nFare thee well, matey! May yer portfolios always prosper!")
            break
        
        if not validate_ticker(ticker_input):
            print("\nBlimey! That ticker symbol looks fishier than a mermaid's tail!")
            print("Please enter a valid ticker (e.g., AAPL, GOOGL, MSFT)")
            continue
        
        print(f"\nAhoy! Fetchin' data for {ticker_input.upper()}...")
        print("(This might take a moment, patience be a virtue on the high seas)")
        
        tracker = StockTracker(ticker_input)
        
        if not tracker.fetch_stock_data():
            print(f"\nShiver me timbers! Could not fetch data for '{ticker_input.upper()}'!")
            print("Possible reasons:")
            print("  - The ticker symbol might not exist")
            print("  - The stock might be delisted")
            print("  - There be troubles with the seas (network issues)")
            print("  - The API might be takin' a break")
            print("\nPlease check the ticker symbol and try again, ye scallywag!")
            continue
        
        metrics = tracker.calculate_metrics()
        
        if metrics is None:
            print("\nDrat! Not enough data to perform analysis!")
            print("The stock might be too new or there be technical difficulties.")
            continue
        
        status, reasons = tracker.analyze_performance(metrics)
        tracker.display_results(metrics, status, reasons)


if __name__ == "__main__":
    main()
