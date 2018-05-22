from golem.core.deferred import sync_wait
from golem.interface.command import group, Argument, command, CommandResult
from golem.rpc.session import Client


# pylint: disable=no-self-use
@group(name="envs", help="Manage environments")
class Environments(object):
    client: Client

    name = Argument('name', help="Environment name")
    value = Argument(
        'value',
        help="Minimal accepted provider performance (> 0)")

    table_headers = ['name', 'supported', 'active', 'performance',
                     'min accept. perf.', 'description']

    sort = Argument(
        '--sort',
        choices=table_headers,
        optional=True,
        default=None,
        help="Sort environments"
    )

    @command(argument=sort, help="Show environments")
    def show(self, sort):

        deferred = Environments.client.get_environments()
        result = sync_wait(deferred) or []

        values = []

        for env in result:
            values.append([
                env['id'],
                str(env['supported']),
                str(env['accepted']),
                str(env['performance']),
                str(env['min_accepted']),
                env['description']
            ])

        return CommandResult.to_tabular(Environments.table_headers, values,
                                        sort=sort)

    @command(argument=name, help="Enable environment")
    def enable(self, name):
        deferred = Environments.client.enable_environment(name)
        return sync_wait(deferred)

    @command(argument=name, help="Disable environment")
    def disable(self, name):
        deferred = Environments.client.disable_environment(name)
        return sync_wait(deferred)

    @command(argument=name, help="Recount performance for an environment")
    def recount(self, name):
        deferred = Environments.client.run_benchmark(name)
        return sync_wait(deferred, timeout=1800)

    @command(arguments=[name, value],
             help="Sets minimal performance for an environment")
    def min_performance(self, name, value):
        deferred = Environments.client.set_min_performance(value, name)
        return sync_wait(deferred, timeout=10)
