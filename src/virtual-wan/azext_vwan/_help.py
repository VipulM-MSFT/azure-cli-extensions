# --------------------------------------------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# Licensed under the MIT License. See License.txt in the project root for license information.
# --------------------------------------------------------------------------------------------

from knack.help_files import helps


# region VirtualHub
helps['network vhub'] = """
    type: group
    short-summary: Manage virtual hubs.
"""

helps['network vhub create'] = """
    type: command
    short-summary: Create a virtual hub.
"""

helps['network vhub list'] = """
    type: command
    short-summary: List virtual hubs.
"""

helps['network vhub show'] = """
    type: command
    short-summary: Get the details of a virtual hub.
"""

helps['network vhub update'] = """
    type: command
    short-summary: Update settings of a virtual hub.
"""

helps['network vhub delete'] = """
    type: command
    short-summary: Delete a virtual hub.
"""

helps['network vhub connection'] = """
    type: group
    short-summary: Manage virtual hub VNet connections.
"""

helps['network vhub connection create'] = """
    type: command
    short-summary: Create a virtual hub VNet connection.
"""

helps['network vhub connection list'] = """
    type: command
    short-summary: List virtual hub VNet connections.
"""

helps['network vhub connection show'] = """
    type: command
    short-summary: Get the details of a virtual hub VNet connection.
"""

helps['network vhub connection update'] = """
    type: command
    short-summary: Update settings of a virtual hub VNet connection.
"""

helps['network vhub connection delete'] = """
    type: command
    short-summary: Delete a virtual hub VNet connection.
"""
# endregion

# region VirtualWAN
helps['network vwan'] = """
    type: group
    short-summary: Manage virtual WANs.
"""

helps['network vwan create'] = """
    type: command
    short-summary: Create a virtual WAN.
"""

helps['network vwan list'] = """
    type: command
    short-summary: List virtual WANs.
"""

helps['network vwan show'] = """
    type: command
    short-summary: Get the details of a virtual WAN.
"""

helps['network vwan update'] = """
    type: command
    short-summary: Update settings of a virtual WAN.
"""

helps['network vwan delete'] = """
    type: command
    short-summary: Delete a virtual WAN.
"""
# endregion

# region VpnSite
helps['network vpn-site'] = """
    type: group
    short-summary: Manage VPN site configurations.
"""

helps['network vpn-site create'] = """
    type: command
    short-summary: Create a VPN site configuration.
"""

helps['network vpn-site list'] = """
    type: command
    short-summary: List VPN site configurations.
"""

helps['network vpn-site show'] = """
    type: command
    short-summary: Get the details of a VPN site configuration.
"""

helps['network vpn-site update'] = """
    type: command
    short-summary: Update settings of a VPN site configuration.
"""

helps['network vpn-site delete'] = """
    type: command
    short-summary: Delete a VPN site configuration.
"""

helps['network vpn-site download'] = """
    type: command
    short-summary: Provide a SAS-URL to download the configuration for a VPN site.
"""
# endregion
