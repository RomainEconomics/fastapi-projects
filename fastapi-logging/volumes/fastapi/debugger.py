import structlog

logger = structlog.get_logger(__name__)


def initialize_debugger():
    import multiprocessing

    if multiprocessing.current_process().pid > 1:
        import debugpy

        debugging_host = "0.0.0.0"
        debugging_port = 9000

        logger.debug(
            "Attatching remote debugger",
            debugger_host=debugging_host,
            debugger_port=debugging_port,
        )
        debugpy.listen(("0.0.0.0", 9000))
        logger.info(
            "Debugger is waiting for remote attachement",
            debugger_host=debugging_host,
            debugger_port=debugging_port,
        )

        debugpy.wait_for_client()

        logger.info(
            "Debugger is successfully attached",
            debugger_host=debugging_host,
            debugger_port=debugging_port,
        )
