# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

# pylint: disable=line-too-long
from azure.cli.core.commands import CliCommandType

from ._client_factory import cf_virtual_wans, cf_virtual_hubs, cf_vpn_sites, cf_vpn_site_configs


# pylint: disable=too-many-locals, too-many-statements
def load_command_table(self, _):

    network_vhub_sdk = CliCommandType(
        operations_tmpl='azure.mgmt.network.operations.virtual_hubs_operations#VirtualHubsOperations.{}',
        client_factory=cf_virtual_hubs,
        min_api='2018-08-01'
    )

    network_vwan_sdk = CliCommandType(
        operations_tmpl='azure.mgmt.network.operations.virtual_wans_operations#VirtualWansOperations.{}',
        client_factory=cf_virtual_wans,
        min_api='2018-08-01'
    )

    network_vpn_site_sdk = CliCommandType(
        operations_tmpl='azure.mgmt.network.operations.vpn_sites_operations#VpnSitesOperations.{}',
        client_factory=cf_vpn_sites,
        min_api='2018-08-01'
    )

    network_vpn_site_config_sdk = CliCommandType(
        operations_tmpl='azure.mgmt.network.operations.vpn_sites_configuration_operations#VpnSitesConfigurationOperations.{}',
        client_factory=cf_vpn_site_configs,
        min_api='2018-08-01'
    )

    # region VirtualWANs
    with self.command_group('network vwan', network_vwan_sdk) as g:
        g.custom_command('create', 'create_virtual_wan')
        g.command('delete', 'delete')
        g.show_command('show')
        g.custom_command('list', 'list_virtual_wans')
        g.generic_update_command('update', custom_func_name='update_virtual_wan')
    # endregion

    # region VirtualHubs
    with self.command_group('network vhub', network_vhub_sdk) as g:
        g.custom_command('create', 'create_virtual_hub')
        g.command('delete', 'delete')
        g.show_command('show')
        g.custom_command('list', 'list_virtual_hubs')
        g.generic_update_command('update', custom_func_name='update_virtual_hub', setter_arg_name='virtual_hub_parameters')

    with self.command_group('network vhub connection', network_vhub_sdk) as g:
        g.custom_command('create', 'create_hub_vnet_connection')
    # endregion

    # region VpnSites
    with self.command_group('network vpn-site', network_vpn_site_sdk) as g:
        g.custom_command('create', 'create_vpn_site')
        g.command('delete', 'delete')
        g.custom_command('list', 'list_vpn_sites')
        g.show_command('show')
        g.generic_update_command('update', custom_func_name='update_vpn_site', setter_arg_name='vpn_site_parameters')

    with self.command_group('network vpn-site', network_vpn_site_config_sdk) as g:
        g.command('download', 'download')
    # endregion