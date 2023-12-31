"""
    Generate Configuration
"""
from package.data_file_functions import read_user_data_file, write_user_data_file


def generate_config(session):
    # Get user data
    user_data = read_user_data_file(session["firewall_name"])

    # Create firewall configuration
    config = []

    if user_data == {}:
        config.append(
            "Empty rule set.  Start by adding a Table using the button on the right."
        )

    # Work through each IP Version, Table and Rule adding to config
    for ip_version in user_data:
        config.append(f"#\n#\n# {ip_version.upper()}\n#\n#\n")

        if "groups" in user_data[ip_version]:
            config.append(f"#\n# Groups\n#")
            for group_name in user_data[ip_version]["groups"]:
                # Get Values
                group_desc = user_data[ip_version]["groups"][group_name]["group_desc"]
                group_type = user_data[ip_version]["groups"][group_name]["group_type"]
                group_value = user_data[ip_version]["groups"][group_name]["group_value"]

                if group_type == "address-group":
                    value_type = "address"
                if group_type == "network-group":
                    value_type = "network"
                if group_type == "port-group":
                    value_type = "port"

                config.append(f"\n# Group: {group_name}")

                # Write Config Statements
                if ip_version == "ipv4":
                    config.append(
                        f"set firewall group {group_type} {group_name} description '{group_desc}'"
                    )
                    for value in group_value:
                        config.append(
                            f"set firewall group {group_type} {group_name} {value_type} '{value}'"
                        )

                if ip_version == "ipv6":
                    config.append(
                        f"set firewall group {ip_version}-{group_type} {group_name} description '{group_desc}'"
                    )
                    for value in group_value:
                        config.append(
                            f"set firewall group {ip_version}-{group_type} {group_name} {value_type} '{value}'"
                        )

            config.append("")

        if "filters" in user_data[ip_version]:
            for filter_name in user_data[ip_version]["filters"]:
                # Get Values
                filter_desc = user_data[ip_version]["filters"][filter_name][
                    "description"
                ]
                filter_action = user_data[ip_version]["filters"][filter_name][
                    "default-action"
                ]
                filter_log = user_data[ip_version]["filters"][filter_name]["log"]

                # Write Config Statements
                config.append(f"#\n# Filter: {filter_name}\n#")
                config.append(
                    f"set firewall {ip_version} {filter_name} filter descriptionn '{filter_desc}'"
                )
                config.append(
                    f"set firewall {ip_version} {filter_name} filter default-action '{filter_action}'"
                )
                if filter_log:
                    config.append(
                        f"set firewall {ip_version} {filter_name} filter enable-default-log"
                    )
                config.append("\n")

                for rule in user_data[ip_version]["filters"][filter_name]["rule-order"]:
                    for key in user_data[ip_version]["filters"][filter_name]["rules"][
                        rule
                    ]:
                        # Get Values
                        description = user_data[ip_version]["filters"][filter_name][
                            "rules"
                        ][rule]["description"]
                        log = (
                            True
                            if "log"
                            in user_data[ip_version]["filters"][filter_name]["rules"][
                                rule
                            ]
                            else False
                        )
                        rule_disable = (
                            True
                            if "rule_disable"
                            in user_data[ip_version]["filters"][filter_name]["rules"][
                                rule
                            ]
                            else False
                        )
                        action = user_data[ip_version]["filters"][filter_name]["rules"][
                            rule
                        ]["action"]
                        interface = user_data[ip_version]["filters"][filter_name][
                            "rules"
                        ][rule]["interface"]
                        direction = user_data[ip_version]["filters"][filter_name][
                            "rules"
                        ][rule]["direction"]
                        jump_target = user_data[ip_version]["filters"][filter_name][
                            "rules"
                        ][rule]["fw_table"]

                    # Write Config Statements
                    config.append(f"# Rule {rule}")

                    # Description
                    config.append(
                        f"set firewall {ip_version} {filter_name} filter rule {rule} description '{description}'"
                    )

                    # Action
                    config.append(
                        f"set firewall {ip_version} {filter_name} filter rule {rule} action '{action}'"
                    )

                    # Interface / Directions
                    if direction == "inbound":
                        config.append(
                            f"set firewall {ip_version} {filter_name} filter rule {rule} inbound-interface '{interface}'"
                        )
                    if direction == "outbound":
                        config.append(
                            f"set firewall {ip_version} {filter_name} filter rule {rule} outbound-interface '{interface}'"
                        )
                    config.append(
                        f"set firewall {ip_version} {filter_name} filter rule {rule} jump-target '{jump_target}'"
                    )

                    # Disable
                    if rule_disable:
                        config.append(
                            f"set firewall {ip_version} {filter_name} filter rule {rule} disable"
                        )

                    # Log
                    if log:
                        config.append(
                            f"set firewall {ip_version} {filter_name} filter rule {rule} log"
                        )
                    config.append("\n")

        if "tables" in user_data[ip_version]:
            for fw_table in user_data[ip_version]["tables"]:
                config.append(f"#\n# Table: {fw_table}\n#")

                if "default" in user_data[ip_version]["tables"][fw_table]:
                    description = user_data[ip_version]["tables"][fw_table]["default"][
                        "description"
                    ]
                    default_action = user_data[ip_version]["tables"][fw_table][
                        "default"
                    ]["default_action"]
                    config.append(
                        f"set firewall {ip_version} name {fw_table} default-action '{default_action}'"
                    )
                    config.append(
                        f"set firewall {ip_version} name {fw_table} description '{description}'"
                    )
                    config.append("\n")

                for rule in user_data[ip_version]["tables"][fw_table]["rule-order"]:
                    for key in user_data[ip_version]["tables"][fw_table][rule]:
                        # Get Values
                        description = user_data[ip_version]["tables"][fw_table][rule][
                            "description"
                        ]
                        rule_disable = (
                            True
                            if "rule_disable"
                            in user_data[ip_version]["tables"][fw_table][rule]
                            else False
                        )
                        logging = (
                            True
                            if "logging"
                            in user_data[ip_version]["tables"][fw_table][rule]
                            else False
                        )
                        action = user_data[ip_version]["tables"][fw_table][rule][
                            "action"
                        ]
                        dest_address = user_data[ip_version]["tables"][fw_table][rule][
                            "dest_address"
                        ]
                        dest_address_type = user_data[ip_version]["tables"][fw_table][
                            rule
                        ]["dest_address_type"]
                        dest_port = user_data[ip_version]["tables"][fw_table][rule][
                            "dest_port"
                        ]
                        dest_port_type = user_data[ip_version]["tables"][fw_table][
                            rule
                        ]["dest_port_type"]
                        source_address = user_data[ip_version]["tables"][fw_table][
                            rule
                        ]["source_address"]
                        source_address_type = user_data[ip_version]["tables"][fw_table][
                            rule
                        ]["source_address_type"]
                        source_port = user_data[ip_version]["tables"][fw_table][rule][
                            "source_port"
                        ]
                        source_port_type = user_data[ip_version]["tables"][fw_table][
                            rule
                        ]["source_port_type"]
                        protocol = user_data[ip_version]["tables"][fw_table][rule][
                            "protocol"
                        ]
                        state_est = (
                            True
                            if "state_est"
                            in user_data[ip_version]["tables"][fw_table][rule]
                            else False
                        )
                        state_inv = (
                            True
                            if "state_inv"
                            in user_data[ip_version]["tables"][fw_table][rule]
                            else False
                        )
                        state_new = (
                            True
                            if "state_new"
                            in user_data[ip_version]["tables"][fw_table][rule]
                            else False
                        )
                        state_rel = (
                            True
                            if "state_rel"
                            in user_data[ip_version]["tables"][fw_table][rule]
                            else False
                        )

                    # Write Config Statements
                    config.append(f"# Rule {rule}")

                    # Disable
                    if rule_disable:
                        config.append(
                            f"set firewall {ip_version} name {fw_table} rule {rule} disable"
                        )

                    # Description
                    config.append(
                        f"set firewall {ip_version} name {fw_table} rule {rule} description '{description}'"
                    )

                    # Action
                    config.append(
                        f"set firewall {ip_version} name {fw_table} rule {rule} action '{action}'"
                    )

                    # Destination
                    if dest_address != "":
                        if dest_address_type == "address":
                            config.append(
                                f"set firewall {ip_version} name {fw_table} rule {rule} destination address '{dest_address}'"
                            )
                        elif dest_address_type == "address_group":
                            config.append(
                                f"set firewall {ip_version} name {fw_table} rule {rule} destination group address-group '{dest_address}'"
                            )
                        elif dest_address_type == "network_group":
                            config.append(
                                f"set firewall {ip_version} name {fw_table} rule {rule} destination group network-group '{dest_address}'"
                            )
                    if dest_port != "":
                        if dest_port_type == "port":
                            config.append(
                                f"set firewall {ip_version} name {fw_table} rule {rule} destination port '{dest_port}'"
                            )
                        elif dest_port_type == "port_group":
                            config.append(
                                f"set firewall {ip_version} name {fw_table} rule {rule} destination group port-group {dest_port}"
                            )

                    # Source
                    if source_address != "":
                        if source_address_type == "address":
                            config.append(
                                f"set firewall {ip_version} name {fw_table} rule {rule} source address '{source_address}'"
                            )
                        elif source_address_type == "address_group":
                            config.append(
                                f"set firewall {ip_version} name {fw_table} rule {rule} source group address-group '{source_address}'"
                            )
                        elif source_address_type == "network_group":
                            config.append(
                                f"set firewall {ip_version} name {fw_table} rule {rule} source group network-group '{source_address}'"
                            )
                    if source_port != "":
                        if source_port_type == "port":
                            config.append(
                                f"set firewall {ip_version} name {fw_table} rule {rule} source port '{source_port}'"
                            )
                        elif source_port_type == "port_group":
                            config.append(
                                f"set firewall {ip_version} name {fw_table} rule {rule} source group port-group '{source_port}'"
                            )

                    # Protocol
                    if protocol != "":
                        if ip_version == "ipv6" and protocol == "icmp":
                            protocol = "ipv6-icmp"
                        config.append(
                            f"set firewall {ip_version} name {fw_table} rule {rule} protocol '{protocol}'"
                        )

                    # Logging
                    if logging:
                        config.append(
                            f"set firewall {ip_version} name {fw_table} rule {rule} log"
                        )

                    # States
                    if state_est:
                        config.append(
                            f"set firewall {ip_version} name {fw_table} rule {rule} state 'established'"
                        )
                    if state_inv:
                        config.append(
                            f"set firewall {ip_version} name {fw_table} rule {rule} state 'invalid'"
                        )
                    if state_new:
                        config.append(
                            f"set firewall {ip_version} name {fw_table} rule {rule} state 'new'"
                        )
                    if state_rel:
                        config.append(
                            f"set firewall {ip_version} name {fw_table} rule {rule} state 'related'"
                        )
                    config.append("")

    # Convert list of lines to single string
    message = ""
    for line in config:
        message = message + line.replace("\n", "<br>") + "<br>"

    # Return message of config commands
    return message
