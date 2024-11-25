from jgmd.logging import LogLevel, Color, FreeTextLogger
from jgmd.events import EventEmitter, getEmitter, handleError, handleErrorAsync
from jgmd.util import loadEnv
import asyncio
from pydantic import BaseModel


async def run():

    # use the logging module
    logger = FreeTextLogger(
        logDirectory="./logs", fileName="logger.log", logLevel=LogLevel.DEBUG
    )
    logger.clearLog()
    logger.logDebug(lambda: f"Hello World!")

    # use the events module
    def onError(event: str, *args, **kwargs):
        logger.logError(lambda: f"An error occurred: {args[0]}")

    eventEmitter: EventEmitter = getEmitter("error", onError)

    def onTestEvent(event: str, *args, **kwargs):
        pass
        logger.logDebug(
            lambda: f"Event {event} emitted w/ args {args} and kwargs {kwargs}!",
            Color.GREEN,
        )
        if True:
            logger.logDebug(lambda: "Emitting a test error!")
            raise Exception("This is a FIRST test error!")

    async def onTestEventAsync(event: str, *args, **kwargs):
        logger.logDebug(
            lambda: f"ASYNC Event {event} emitted w/ args {args} and kwargs {kwargs}!",
            Color.GREEN,
        )
        logger.logDebug(lambda: "ASYNC #1 Sleeping for 3 seconds...", Color.YELLOW)
        await asyncio.sleep(3)
        logger.logDebug(lambda: "ASYNC #1 Done sleeping.", Color.YELLOW)
        if True:
            logger.logDebug(lambda: "ASYNC Emitting a test error!")
            raise Exception("This is a ASYNC test error!")

    async def onTestEventAsync2(event: str, *args, **kwargs):
        logger.logDebug(lambda: "ASYNC #2 Sleeping for 3 seconds...", Color.YELLOW)
        await asyncio.sleep(3)
        logger.logDebug(lambda: "ASYNC #2 Done sleeping.", Color.YELLOW)

    EVENT_NAME = "test"
    eventEmitter.on(EVENT_NAME, onTestEventAsync)
    eventEmitter.on(EVENT_NAME, onTestEvent)
    eventEmitter.on(EVENT_NAME, onTestEventAsync2)
    eventEmitter.emit(EVENT_NAME, 1, 2, 3, otherStuff="hello")

    logger.logDebug(lambda: "End of event test.")

    @handleError
    def trySomething():
        logger.logDebug(lambda: "Trying something...")
        if True:
            raise Exception("This is a SECOND test error!")

    @handleErrorAsync
    async def trySomethingAsync():
        logger.logDebug(lambda: "Trying something async...")
        if True:
            raise Exception("This is a THIRD test error!")

    trySomething()

    await trySomethingAsync()

    # use the loadEnv utility fxn
    class Env(BaseModel):
        logDirectory: str
        logLevel: str
        twsApiIp: str
        twsApiPort: int
        watchlistFile: str
        notificationSoundsFile: str
        defaultThresholdsFile: str
        overrideThresholdsFile: str
        pushoverUserKey: str
        pushoverApiToken: str

    # Load config
    env_config = loadEnv(Env)

    print(env_config)

    await asyncio.sleep(5)
    logger.logDebug(lambda: "End of script.")


asyncio.run(run())
