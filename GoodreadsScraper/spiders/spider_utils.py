"""Utility functions for spiders"""

def report_progress_every_n(logger, metric_name, metric, n):
    if metric % n == 0:
        logger.info("%d %s parsed till now.", metric, metric_name)
