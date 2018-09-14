# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from knack.util import CLIError
from knack.log import get_logger

from ._client_factory import network_client_factory


logger = get_logger(__name__)


class UpdateContext(object):

    def __init__(self, instance):
        self.instance = instance

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        pass

    def update_param(self, prop, value, allow_clear):
        if value == '' and allow_clear:
            setattr(self.instance, prop, None)
        elif value is not None:
            setattr(self.instance, prop, value)


def _generic_list(cli_ctx, operation_name, resource_group_name):
    ncf = network_client_factory(cli_ctx)
    operation_group = getattr(ncf, operation_name)
    if resource_group_name:
        return operation_group.list_by_resource_group(resource_group_name)

    return operation_group.list()


def _get_property(items, name):
    result = next((x for x in items if x.name.lower() == name.lower()), None)
    if not result:
        raise CLIError("Property '{}' does not exist".format(name))
    else:
        return result


def _upsert(parent, collection_name, obj_to_add, key_name, warn=True):
    if not getattr(parent, collection_name, None):
        setattr(parent, collection_name, [])
    collection = getattr(parent, collection_name, None)

    value = getattr(obj_to_add, key_name)
    if value is None:
        raise CLIError(
            "Unable to resolve a value for key '{}' with which to match.".format(key_name))
    match = next((x for x in collection if getattr(x, key_name, None) == value), None)
    if match:
        if warn:
            logger.warning("Item '%s' already exists. Replacing with new values.", value)
        collection.remove(match)

    collection.append(obj_to_add)


def _find_item_at_path(instance, path):
    # path accepts the pattern property/name/property/name
    curr_item = instance
    path_comps = path.split('.')
    for i, comp in enumerate(path_comps):
        if i % 2:
            # name
            curr_item = next((x for x in curr_item if x.name == comp), None)
        else:
            # property
            curr_item = getattr(curr_item, comp, None)
        if not curr_item:
            raise CLIError("unable to find '{}'...".format(comp))
    return curr_item



# region P2SVpnGateway
def create_p2s_vpn_gateway(cmd, resource_group_name, vpn_gateway_name,
                           location=None, tags=None):
    client = network_client_factory(cmd.cli_ctx).p2s_vpn_gateways
    P2sVpnGatewaysOperations = cmd.get_models('P2sVpnGatewaysOperations')
    gateway = P2sVpnGatewaysOperations(
        location=location,
        tags=tags
    )
    return client.create_or_update(resource_group_name, vpn_gateway_name, gateway)
# endregion


# region VirtualNetworkConnections
def create_hub_vnet_connection(cmd, resource_group_name, virtual_hub_name, connection_name, remote_virtual_network,
                               allow_hub_to_remote_vnet_transit=None, allow_remote_vnet_to_use_hub_vnet_gateways=None,
                               enable_internet_security=None):
    HubVirtualNetworkConnection, SubResource = cmd.get_models(
        'HubVirtualNetworkConnection', 'SubResource')
    client = network_client_factory(cmd.cli_ctx).virtual_hubs
    hub = client.get(resource_group_name, virtual_hub_name)
    connection = HubVirtualNetworkConnection(
        name=connection_name,
        remote_virtual_network=SubResource(id=remote_virtual_network),
        allow_hub_to_remote_vnet_transit=allow_hub_to_remote_vnet_transit,
        allow_remote_vnet_to_use_hub_vnet_gateway=allow_remote_vnet_to_use_hub_vnet_gateways,
        enable_internet_security=enable_internet_security
    )
    _upsert(hub, 'virtual_network_connections', connection, 'name', warn=True)
    poller = client.create_or_update(resource_group_name, virtual_hub_name, hub)
    return _get_property(poller.result().virtual_network_connections, connection_name)
# endregion


# region VirtualWAN
def create_virtual_wan(cmd, resource_group_name, virtual_wan_name, tags=None, location=None,
                       security_provider_name=None, branch_to_branch_traffic=None,
                       vnet_to_vnet_traffic=None, office365_category=None, disable_vpn_encryption=None):
    client = network_client_factory(cmd.cli_ctx).virtual_wans
    VirtualWAN = cmd.get_models('VirtualWAN')
    wan = VirtualWAN(
        tags=tags,
        location=location,
        disable_vpn_encryption=disable_vpn_encryption,
        security_provider_name=security_provider_name,
        allow_branch_to_branch_traffic=branch_to_branch_traffic,
        allow_vnet_to_vnet_traffic=vnet_to_vnet_traffic,
        office365_local_breakout_category=office365_category
    )
    return client.create_or_update(resource_group_name, virtual_wan_name, wan)


def update_virtual_wan(instance, tags=None, security_provider_name=None, branch_to_branch_traffic=None,
                       vnet_to_vnet_traffic=None, office365_category=None, disable_vpn_encryption=None):
    with UpdateContext(instance) as c:
        c.update_param('tags', tags, True)
        c.update_param('security_provider_name', security_provider_name, False)
        c.update_param('allow_branch_to_branch_traffic', branch_to_branch_traffic, False)
        c.update_param('allow_vnet_to_vnet_traffic', vnet_to_vnet_traffic, False)
        c.update_param('office365_local_breakout_category', office365_category, False)
        c.update_param('disable_vpn_encryption', disable_vpn_encryption, False)
    return instance


def list_virtual_wans(cmd, resource_group_name=None):
    client = network_client_factory(cmd.cli_ctx).virtual_wans
    if resource_group_name:
        return client.list_by_resource_group(resource_group_name)
    return client.list()
# endregion


# region VirtualHubs
def create_virtual_hub(cmd, resource_group_name, virtual_hub_name, address_prefix, virtual_wan,
                       location=None, tags=None, express_route_gateway=None, p2s_vpn_gateway=None,
                       vpn_gateway=None):
    client = network_client_factory(cmd.cli_ctx).virtual_hubs
    VirtualHub, SubResource = cmd.get_models('VirtualHub', 'SubResource')
    hub = VirtualHub(
        tags=tags,
        location=location,
        address_prefix=address_prefix,
        virtual_wan=SubResource(id=virtual_wan),
        express_route_gateway=SubResource(id=express_route_gateway) if express_route_gateway else None,
        p2_svpn_gatway=SubResource(id=p2s_vpn_gateway) if p2s_vpn_gateway else None,
        vpn_gateway=SubResource(id=vpn_gateway) if vpn_gateway else None
    )
    return client.create_or_update(resource_group_name, virtual_hub_name, hub)


def update_virtual_hub(instance, cmd, address_prefix=None, virtual_wan=None, tags=None,
                       vpn_gateway=None, express_route_gateway=None, p2s_vpn_gateway=None):
    SubResource = cmd.get_models('SubResource')
    with UpdateContext(instance) as c:
        c.update_param('tags', tags, True)
        c.update_param('address_prefix', address_prefix, False)
        c.update_param('virtual_wan', SubResource(id=virtual_wan) if virtual_wan else None, False)
        c.update_param('express_route_gateway',
            SubResource(id=express_route_gateway) if express_route_gateway else None, True)
        c.update_param('vpn_gateway', SubResource(id=vpn_gateway) if vpn_gateway else None, True)
        c.update_param('p2_svpn_gateway', SubResource(id=p2s_vpn_gateway) if p2s_vpn_gateway else None, True)
    return instance


def list_virtual_hubs(cmd, resource_group_name=None):
    client = network_client_factory(cmd.cli_ctx).virtual_hubs
    if resource_group_name:
        return client.list_by_resource_group(resource_group_name)
    return client.list()
# endregion


# region VpnGateways
def create_vpn_gateway(cmd, resource_group_name, gateway_name,
                       location=None, tags=None):
    client = network_client_factory(cmd.cli_ctx).vpn_gateways
    VpnGateway = cmd.get_models('VpnGateway')
    gateway = VpnGateway(
        location=location,
        tags=tags
    )
    return client.create_or_update(resource_group_name, gateway_name, gateway)
# endregion


# region VpnSites
def create_vpn_site(cmd, resource_group_name, vpn_site_name, ip_address,
                    asn, bgp_peering_address,
                    virtual_wan=None, location=None, tags=None,
                    site_key=None, address_prefixes=None, is_security_site=None,
                    device_vendor=None, device_model=None, link_speed=None,
                    peer_weight=None):
    client = network_client_factory(cmd.cli_ctx).vpn_sites
    VpnSite, SubResource = cmd.get_models('VpnSite', 'SubResource')
    site = VpnSite(
        location=location,
        tags=tags,
        is_security_site=is_security_site,
        ip_address=ip_address,
        site_key=site_key,
        virtual_wan=SubResource(id=virtual_wan) if virtual_wan else None,
        address_space={'addressPrefixes': address_prefixes},
        device_properties={
            'deviceVendor': device_vendor,
            'deviceModel': device_model,
            'linkSpeedInMbps': link_speed
        },
        bgp_properties={
            'asn': asn,
            'bgpPeeringAddress': bgp_peering_address,
            'peerWeight': peer_weight
        }
    )
    return client.create_or_update(resource_group_name, vpn_site_name, site)


def update_vpn_site(instance, cmd, ip_address=None, virtual_wan=None, tags=None,
                    site_key=None, address_prefixes=None, is_security_site=None,
                    device_vendor=None, device_model=None, link_speed=None,
                    asn=None, bgp_peering_address=None, peer_weight=None):
    SubResource = cmd.get_models('SubResource')
    with UpdateContext(instance) as c:
        c.update_param('tags', tags, True)
        c.update_param('ip_address', ip_address, False)
        c.update_param('virtual_wan', SubResource(id=virtual_wan) if virtual_wan else None, False)
        c.update_param('is_security_site', is_security_site, False)
        c.update_param('site_key', site_key, True)

    device_properties = instance.device_properties
    with UpdateContext(device_properties) as c:
        c.update_param('device_vendor', device_vendor, True)
        c.update_param('device_model', device_model, True)
        c.update_param('link_speed_in_mbps', link_speed, False)

    address_space = instance.address_space
    with UpdateContext(address_space) as c:
        c.update_param('address_prefixes', address_prefixes, False)

    bgp_properties = instance.bgp_properties
    with UpdateContext(bgp_properties) as c:
        c.update_param('asn', asn, False)
        c.update_param('bgp_peering_address', bgp_peering_address, False)
        c.update_param('peer_weight', peer_weight, False)

    return instance


def list_vpn_sites(cmd, resource_group_name=None):
    client = network_client_factory(cmd.cli_ctx).vpn_sites
    if resource_group_name:
        return client.list_by_resource_group(resource_group_name)
    return client.list()
# endregion
