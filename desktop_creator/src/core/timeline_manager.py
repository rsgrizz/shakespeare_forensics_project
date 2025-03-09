    def _create_relationship_mapping(self, play_name: str) -> Dict:
        """Create modern relationship mappings"""
        relationships = {
            "julius_caesar": {
                "CAESAR": {
                    "allies": ["ANTONY", "CALPURNIA"],
                    "opponents": ["BRUTUS", "CASSIUS"],
                    "subordinates": ["CINNA", "DECIUS"]
                },
                "BRUTUS": {
                    "allies": ["CASSIUS", "CICERO"],
                    "opponents": ["CAESAR", "ANTONY"],
                    "subordinates": ["LUCIUS"]
                }
            },
            "hamlet": {
                "HAMLET": {
                    "allies": ["HORATIO", "OPHELIA"],
                    "opponents": ["CLAUDIUS", "POLONIUS"],
                    "subordinates": ["ROSENCRANTZ", "GUILDENSTERN"]
                },
                "CLAUDIUS": {
                    "allies": ["POLONIUS", "GERTRUDE"],
                    "opponents": ["HAMLET"],
                    "subordinates": ["OSRIC"]
                }
            }
        }

        return relationships.get(play_name, {})

    def _modernize_relationships(self, character: str, relationships: Dict) -> Dict:
        """Convert relationships to modern context"""
        modern_rels = {
            "reports_to": [],
            "supervises": [],
            "collaborates_with": [],
            "conflicts_with": []
        }

        # Convert traditional relationships to modern organizational relationships
        if "allies" in relationships:
            modern_rels["collaborates_with"] = relationships["allies"]
        if "opponents" in relationships:
            modern_rels["conflicts_with"] = relationships["opponents"]
        if "subordinates" in relationships:
            modern_rels["supervises"] = relationships["subordinates"]

        return modern_rels

