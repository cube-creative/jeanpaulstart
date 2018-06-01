import os.path
from unittest import TestCase
from jeanpaulstart import batch
from jeanpaulstart import plugin_loader
from jeanpaulstart import async_executor
from jeanpaulstart.constants import *


HERE = os.path.dirname(__file__)


class TestAsyncExecutor(TestCase):

    def setUp(self):
        plugin_loader.init(force=True)
        self.batch_ok = batch.from_filepath(HERE + "/batches/async_ok.yml")

    def test_run_async_steps(self):
        #
        # Init
        executor = async_executor.AsyncExecutor(batch=self.batch_ok)

        self.assertEqual(
            executor.status(),
            ASYNC_EXEC_READY
        )

        self.assertEqual(
            executor.progress(),
            0
        )

        #
        ## Step 0
        executor.start()

        self.assertEqual(
            executor.status(),
            ASYNC_EXEC_RUNNING
        )

        self.assertEqual(
            executor.last_message(),
            "[Async OK][From environment] 'environment' with argument(s) name=ENV_VAR1 value=value1"
        )

        self.assertEqual(
            executor.progress(),
            0.0
        )

        #
        ## Step 1
        executor.step()

        self.assertEqual(
            executor.status(),
            ASYNC_EXEC_RUNNING
        )

        self.assertEqual(
            executor.last_message(),
            "[Async OK][From environment] 'environment' with argument(s) name=ENV_VAR1 value=value1"
        )

        self.assertEqual(
            executor.progress(),
            0.33
        )

        #
        ## Step 2
        executor.step()

        self.assertEqual(
            executor.status(),
            ASYNC_EXEC_RUNNING
        )

        self.assertEqual(
            executor.last_message(),
            "[Async OK][From environment] 'environment' with argument(s) name=ENV_VAR2 value=['valuea', 'valueb']"
        )

        self.assertEqual(
            executor.progress(),
            0.66
        )

        #
        ## Step 3
        executor.step()

        self.assertEqual(
            executor.status(),
            ASYNC_EXEC_RUNNING
        )

        self.assertEqual(
            executor.last_message(),
            "[Async OK][Some Task] 'raw' with argument(s) async=False command=some command"
        )

        self.assertEqual(
            executor.progress(),
            1
        )

        #
        # End
        executor.step()

        self.assertEqual(
            executor.status(),
            ASYNC_EXEC_FINISHED
        )

        self.assertEqual(
            executor.last_message(),
            "[Async OK][Backup environment]"
        )

        self.assertEqual(
            executor.progress(),
            1
        )

    def test_run_async_while(self):
        messages = list()
        statuses = list()
        progresses = list()
        executor = async_executor.AsyncExecutor(batch=self.batch_ok)
        executor.start()

        messages.append(executor.last_message())
        statuses.append(executor.status())
        progresses.append(executor.progress())

        while executor.status() == ASYNC_EXEC_RUNNING:
            executor.step()

            messages.append(executor.last_message())
            statuses.append(executor.status())
            progresses.append(executor.progress())

        self.assertEqual(
            executor.status(),
            ASYNC_EXEC_FINISHED
        )

        self.assertEqual(
            messages,
            [
                "[Async OK][From environment] 'environment' with argument(s) name=ENV_VAR1 value=value1",
                "[Async OK][From environment] 'environment' with argument(s) name=ENV_VAR1 value=value1",
                "[Async OK][From environment] 'environment' with argument(s) name=ENV_VAR2 value=['valuea', 'valueb']",
                "[Async OK][Some Task] 'raw' with argument(s) async=False command=some command", '[Async OK][Backup environment]'
            ]
        )

        self.assertEqual(
            statuses,
            [
                ASYNC_EXEC_RUNNING,
                ASYNC_EXEC_RUNNING,
                ASYNC_EXEC_RUNNING,
                ASYNC_EXEC_RUNNING,
                ASYNC_EXEC_FINISHED
            ]
        )

        self.assertEqual(
            progresses,
            [0.0, 0.33, 0.66, 1.0, 1.0]
        )

    def test_run_async_while_offset(self):
        messages = list()
        statuses = list()
        progresses = list()
        executor = async_executor.AsyncExecutor(batch=self.batch_ok)
        executor.message_offset = 1
        executor.start()

        messages.append(executor.last_message())
        statuses.append(executor.status())
        progresses.append(executor.progress())

        while executor.status() == ASYNC_EXEC_RUNNING:
            executor.step()

            messages.append(executor.last_message())
            statuses.append(executor.status())
            progresses.append(executor.progress())

        self.assertEqual(
            executor.status(),
            ASYNC_EXEC_FINISHED
        )

        print messages

        # Todo : ameliorer le doublon !!
        self.assertEqual(
            messages,
            [
                "[Async OK][From environment] 'environment' with argument(s) name=ENV_VAR2 value=['valuea', 'valueb']",
                "[Async OK][From environment] 'environment' with argument(s) name=ENV_VAR2 value=['valuea', 'valueb']",
                "[Async OK][Some Task] 'raw' with argument(s) async=False command=some command",
                "[Async OK][Some Task] 'raw' with argument(s) async=False command=some command",
                "[Async OK][Backup environment]"
            ]
        )

        self.assertEqual(
            statuses,
            [
                ASYNC_EXEC_RUNNING,
                ASYNC_EXEC_RUNNING,
                ASYNC_EXEC_RUNNING,
                ASYNC_EXEC_RUNNING,
                ASYNC_EXEC_FINISHED
            ]
        )

        self.assertEqual(
            progresses,
            [0.0, 0.33, 0.66, 1.0, 1.0]
        )
