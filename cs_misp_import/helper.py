"""Helper methods."""

try:
    from pymisp import MISPObject, MISPAttribute
except ImportError as no_pymisp:
    raise SystemExit(
        "The PyMISP package must be installed to use this program."
        ) from no_pymisp

def gen_indicator(indicator, tag_list) -> MISPObject or MISPAttribute:
        """Create the appropriate MISP event object for the indicator (based upon type)."""
        if not indicator.get('type') or not indicator.get('indicator'):
            return False

        indicator_type = indicator.get('type')
        indicator_value = indicator.get('indicator')
        indicator_first = indicator.get("published_date", 0)
        indicator_last = indicator.get("last_updated", 0)
        # Type, Object_Type, Attribute Name
        ind_objects = [
            # ["hash_md5", "file", "md5"],
            # ["hash_sha256", "file", "sha256"],
            # ["hash_sha1", "file", "sha1"],
            # ["file_name", "file", "filename"],
            # ["mutex_name", "mutex", "name"],
            ["password", "credential", "password"],
            # ["url", "url", "url"],
            # ["email_address", "email", "reply-to"],
            ["username", "credential", "username"],
            # ["bitcoin_address", "btc-transaction", "btc-address"],
            # ["registry", "registry-key", "key"],
            ["x509_serial", "x509", "serial-number"],
            # ["file_path", "file", "fullpath"],
            # ["email_subject", "email", "subject"],
            # ["coin_address", "coin-address", "address"],
            ["x509_subject", "x509", "subject"],
            #["device_name", "device", "name"],
            # ["hash_imphash", "pe", "imphash"]
        ]

        for ind_obj in ind_objects:
            if indicator_type == ind_obj[0]:
                indicator_object = MISPObject(ind_obj[1])
                att = indicator_object.add_attribute(ind_obj[2], indicator_value)
                if indicator_first:
                    att.first_seen = indicator_first
                if indicator_last:
                    att.last_seen = indicator_last
                att.add_tag(f"CrowdStrike:indicator: {ind_obj[2].lower()}")
                for tag in tag_list:
                    att.add_tag(tag)

                return indicator_object

        # Type, Category, Attribute Type
        ind_attributes = [
            ["hash_md5", "Artifacts dropped", "md5"],
            ["hash_sha256", "Artifacts dropped", "sha256"],
            ["hash_sha1", "Artifacts dropped", "sha1"],
            ["hash_imphash", "Artifacts dropped", "imphash"],
            ["file_name", "Artifacts dropped", "filename"],
            ["file_path", "Payload delivery", "filename"],
            ["url", "Network activity", "url"],
            ["mutex_name", "Artifacts dropped", "mutex"],
            ["bitcoin_address", "Financial fraud", "btc"],
            ["coin_address", "Financial fraud", "bic"],
            ["email_address", "Payload delivery", "email-reply-to"],
            ["email_subject", "Payload delivery", "email-subject"],
            ["registry", "Persistence mechanism", "regkey"],
            ["device_name", "Targeting data", "target-machine"],
            ["domain", "Network activity", "domain"],
            ["campaign_id", "Attribution", "campaign-id"],
            ["ip_address", "Network activity", "ip-src"],
            ["service_name", "Artifacts Dropped", "windows-service-name"],
            ["user_agent", "Network activity", "user-agent"],
            ["port", "Network activity", "port"]
        ]

        for ind_att in ind_attributes:
            if indicator_type == ind_att[0]:
                indicator_attribute = MISPAttribute()
                indicator_attribute.category = ind_att[1]
                indicator_attribute.type = ind_att[2]
                indicator_attribute.value = indicator_value

                return indicator_attribute

        return False