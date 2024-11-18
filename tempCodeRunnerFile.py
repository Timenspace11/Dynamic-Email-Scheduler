@app.before_first_request
def start_scheduler():
    # Run the scheduler in a separate thread to not block the Flask app
    threading.Thread(target=run_scheduler, daemon=True).start()