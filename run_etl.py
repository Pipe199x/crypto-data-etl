import time
import schedule
from etl.coingecko_etl import run_etl
from config import CRYPTOCURRENCIES_TO_FETCH

def scheduled_etl():
    """Run the ETL process once and log the start and end times."""
    print(f"Starting scheduled ETL process at {time.strftime('%Y-%m-%d %H:%M:%S')}...")
    run_etl(CRYPTOCURRENCIES_TO_FETCH)
    print(f"Scheduled ETL process completed at {time.strftime('%Y-%m-%d %H:%M:%S')}")

def run_continuous_update():
    """Configure the process to run continuously at defined intervals."""
    print("Starting continuous update process...")

    # Schedule the ETL process to run every 60 seconds
    schedule.every(60).seconds.do(scheduled_etl)

    # Keep the process running indefinitely, checking every second
    while True:
        schedule.run_pending()  # Check for any scheduled tasks
        time.sleep(1)  # Wait 1 second before checking again

if __name__ == "__main__":
    import sys  # Import sys only when running this script directly

    # Check if the "--continuous" argument is passed in the command line
    if len(sys.argv) > 1 and sys.argv[1] == "--continuous":
        # If the argument is present, run the continuous update process
        run_continuous_update()
    else:
        # If no argument is specified, run the ETL process only once
        print("Starting one-time ETL process for cryptocurrency data...")
        run_etl(CRYPTOCURRENCIES_TO_FETCH)
        print("One-time ETL process completed.")
