import os
import sentry_sdk

if os.getenv("PRODUCTION", "False").lower() in ("true", "1", "t"):
    sentry_sdk.init(
        dsn="https://f17c56c681bd044ebea1ca1074eb837c@o555244.ingest.us.sentry.io/4507589807308800",
        traces_sample_rate=0.0,
        profiles_sample_rate=0.0,
    )
