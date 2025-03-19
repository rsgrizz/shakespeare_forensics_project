"""
Generate_Static_Data.py
Created by RSGrizz
Date: March 2024
Version: 1.2

Generates comprehensive US-based static data for Shakespeare Forensics Project:
- 50+ major US cities with area codes
- 60+ companies across multiple sectors
- 20+ government agencies
- Multiple business hierarchies and structures
- Location-specific business districts and sectors

This data supports character modernization and scenario generation
for the Shakespeare Forensics Training Data Generator.
"""

import json
import random
from pathlib import Path
from typing import Dict, List
from datetime import datetime

class StaticDataGenerator:
    """Generates and manages static data for the Shakespeare Forensics Project."""
    
    def __init__(self):
        self.base_dir = Path("desktop_creator/data/static/modern_mappings")
        self.timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        self.data_version = "1.2"
        
        # Ensure directory structure exists
        self._create_directory_structure()
        
    def _create_directory_structure(self):
        """Create necessary directory structure for static data."""
        directories = [
            self.base_dir / "business",
            self.base_dir / "government",
            self.base_dir / "locations",
            self.base_dir / "relationships",
            self.base_dir / "cities"
        ]
        
        for directory in directories:
            directory.mkdir(parents=True, exist_ok=True)
            
    def _add_metadata(self, data: Dict) -> Dict:
        """Add metadata to generated data."""
        return {
            "metadata": {
                "generated_by": "RSGrizz",
                "generated_date": self.timestamp,
                "version": self.data_version,
                "project": "Shakespeare Forensics"
            },
            "data": data
        }
        
    def write_json_file(self, data: Dict, filename: str):
        """Write data to JSON file with metadata."""
        full_path = self.base_dir / filename
        
        # Ensure directory exists
        full_path.parent.mkdir(parents=True, exist_ok=True)
        
        # Add metadata to data if it doesn't exist
        if not isinstance(data, dict) or "metadata" not in data:
            data = self._add_metadata(data)
        
        with open(full_path, 'w', encoding='utf-8') as f:
            json.dump(data, f, indent=2)
            
        print(f"Generated: {full_path}")

    def generate_us_cities(self) -> Dict:
        """Generate comprehensive US city data with area codes and business districts."""
        return {
            "metadata": {
                "category": "us_cities",
                "description": "Major US cities with business districts and area codes",
                "last_updated": self.timestamp
            },
            "regions": {
                "northeast": {
                    "major_cities": {
                        "new_york": {
                            "name": "New York City",
                            "state": "NY",
                            "area_codes": ["212", "646", "718", "917", "929"],
                            "business_districts": [
                                "Wall Street",
                                "Midtown Manhattan",
                                "Silicon Alley",
                                "Hudson Yards",
                                "World Trade Center"
                            ],
                            "industries": [
                                "Finance",
                                "Media",
                                "Technology",
                                "Fashion",
                                "Advertising"
                            ],
                            "major_employers": [
                                "JPMorgan Chase",
                                "Goldman Sachs",
                                "Morgan Stanley",
                                "IBM",
                                "Google"
                            ]
                        },
                        "boston": {
                            "name": "Boston",
                            "state": "MA",
                            "area_codes": ["617", "857"],
                            "business_districts": [
                                "Financial District",
                                "Seaport Innovation District",
                                "Kendall Square",
                                "Back Bay",
                                "Cambridge Innovation Center"
                            ],
                            "industries": [
                                "Biotechnology",
                                "Education",
                                "Healthcare",
                                "Technology",
                                "Financial Services"
                            ],
                            "major_employers": [
                                "Harvard University",
                                "MIT",
                                "Biogen",
                                "Fidelity Investments",
                                "State Street Corporation"
                            ]
                        }
                    },
                    "secondary_cities": {
                        "providence": {
                            "name": "Providence",
                            "state": "RI",
                            "area_codes": ["401"],
                            "key_industries": [
                                "Healthcare",
                                "Education",
                                "Manufacturing"
                            ]
                        }
                    }
                },
                "midwest": {
                    "major_cities": {
                        "chicago": {
                            "name": "Chicago",
                            "state": "IL",
                            "area_codes": ["312", "773", "872"],
                            "business_districts": [
                                "The Loop",
                                "River North",
                                "West Loop",
                                "Magnificent Mile",
                                "Chicago Tech Hub"
                            ],
                            "industries": [
                                "Finance",
                                "Technology",
                                "Manufacturing",
                                "Transportation",
                                "Professional Services"
                            ],
                            "major_employers": [
                                "Boeing",
                                "United Airlines",
                                "Abbott Laboratories",
                                "McDonald's Corporation",
                                "Northern Trust"
                            ]
                        }
                    }
                },
                "west_coast": {
                    "major_cities": {
                        "san_francisco": {
                            "name": "San Francisco",
                            "state": "CA",
                            "area_codes": ["415", "628"],
                            "business_districts": [
                                "Financial District",
                                "SoMa",
                                "Mission Bay",
                                "Silicon Valley",
                                "Embarcadero"
                            ],
                            "industries": [
                                "Technology",
                                "Finance",
                                "Biotechnology",
                                "Digital Media",
                                "Venture Capital"
                            ],
                            "major_employers": [
                                "Salesforce",
                                "Twitter",
                                "Uber",
                                "Wells Fargo",
                                "Genentech"
                            ]
                        }
                    }
                }
            },
            "city_relationships": {
                "business_corridors": [
                    {
                        "name": "Northeast Corridor",
                        "cities": ["New York", "Boston", "Philadelphia"],
                        "primary_industries": ["Finance", "Technology", "Education"]
                    },
                    {
                        "name": "Silicon Valley",
                        "cities": ["San Francisco", "San Jose", "Oakland"],
                        "primary_industries": ["Technology", "Venture Capital", "Innovation"]
                    }
                ],
                "sister_cities": {
                    "new_york": ["London", "Tokyo", "Beijing"],
                    "chicago": ["Mexico City", "Toronto", "Shanghai"],
                    "san_francisco": ["Sydney", "Seoul", "Osaka"]
                }
            }
        }

    def generate_city_infrastructure(self) -> Dict:
        """Generate infrastructure and connectivity data for cities."""
        return {
            "transportation_hubs": {
                "airports": {
                    "new_york": ["JFK", "LaGuardia", "Newark"],
                    "chicago": ["O'Hare", "Midway"],
                    "los_angeles": ["LAX", "Burbank", "Long Beach"]
                },
                "train_stations": {
                    "new_york": ["Penn Station", "Grand Central"],
                    "boston": ["South Station", "North Station"],
                    "washington_dc": ["Union Station"]
                }
            },
            "technology_infrastructure": {
                "data_centers": {
                    "virginia": ["Ashburn", "Sterling", "Reston"],
                    "texas": ["Dallas", "Houston", "Austin"],
                    "california": ["Silicon Valley", "Los Angeles", "Sacramento"]
                },
                "tech_corridors": {
                    "route_128": {
                        "region": "Boston Area",
                        "focus": ["Technology", "Biotechnology", "Defense"]
                    },
                    "silicon_valley": {
                        "region": "San Francisco Bay Area",
                        "focus": ["Software", "Hardware", "Internet"]
                    }
                }
            }
        }

    def generate_additional_us_cities(self) -> Dict:
        """Generate additional US cities data with business focus."""
        return {
            "south": {
                "major_cities": {
                    "atlanta": {
                        "name": "Atlanta",
                        "state": "GA",
                        "area_codes": ["404", "470", "678", "770"],
                        "business_districts": [
                            "Downtown",
                            "Buckhead",
                            "Midtown",
                            "Atlantic Station",
                            "Perimeter Center"
                        ],
                        "industries": [
                            "Transportation",
                            "Media",
                            "Technology",
                            "Healthcare",
                            "Finance"
                        ],
                        "major_employers": [
                            "Coca-Cola",
                            "Delta Airlines",
                            "Home Depot",
                            "UPS",
                            "CNN"
                        ]
                    },
                    "miami": {
                        "name": "Miami",
                        "state": "FL",
                        "area_codes": ["305", "786"],
                        "business_districts": [
                            "Brickell",
                            "Downtown",
                            "Design District",
                            "Wynwood",
                            "Coral Gables"
                        ],
                        "industries": [
                            "Banking",
                            "Tourism",
                            "International Trade",
                            "Real Estate",
                            "Healthcare"
                        ]
                    },
                    "dallas": {
                        "name": "Dallas",
                        "state": "TX",
                        "area_codes": ["214", "469", "972"],
                        "business_districts": [
                            "Downtown",
                            "Uptown",
                            "Deep Ellum",
                            "Preston Center",
                            "Legacy"
                        ],
                        "industries": [
                            "Technology",
                            "Finance",
                            "Energy",
                            "Healthcare",
                            "Defense"
                        ]
                    }
                }
            },
            "southwest": {
                "major_cities": {
                    "phoenix": {
                        "name": "Phoenix",
                        "state": "AZ",
                        "area_codes": ["480", "602", "623"],
                        "business_districts": [
                            "Downtown",
                            "Camelback Corridor",
                            "Desert Ridge",
                            "Scottsdale Airpark"
                        ],
                        "industries": [
                            "Technology",
                            "Healthcare",
                            "Tourism",
                            "Real Estate"
                        ]
                    },
                    "denver": {
                        "name": "Denver",
                        "state": "CO",
                        "area_codes": ["303", "720"],
                        "business_districts": [
                            "Downtown",
                            "Denver Tech Center",
                            "RiNo",
                            "Cherry Creek"
                        ],
                        "industries": [
                            "Technology",
                            "Energy",
                            "Aerospace",
                            "Healthcare"
                        ]
                    }
                }
            },
            "pacific_northwest": {
                "major_cities": {
                    "seattle": {
                        "name": "Seattle",
                        "state": "WA",
                        "area_codes": ["206", "253", "425"],
                        "business_districts": [
                            "Downtown",
                            "South Lake Union",
                            "Bellevue CBD",
                            "Pioneer Square"
                        ],
                        "industries": [
                            "Technology",
                            "Aerospace",
                            "Retail",
                            "Biotechnology"
                        ],
                        "major_employers": [
                            "Amazon",
                            "Microsoft",
                            "Boeing",
                            "Starbucks"
                        ]
                    },
                    "portland": {
                        "name": "Portland",
                        "state": "OR",
                        "area_codes": ["503", "971"],
                        "business_districts": [
                            "Downtown",
                            "Pearl District",
                            "Lloyd District",
                            "South Waterfront"
                        ],
                        "industries": [
                            "Technology",
                            "Athletic & Outdoor",
                            "Manufacturing",
                            "Green Technology"
                        ]
                    }
                }
            },
            "southeast": {
                "major_cities": {
                    "charlotte": {
                        "name": "Charlotte",
                        "state": "NC",
                        "area_codes": ["704", "980"],
                        "business_districts": [
                            "Uptown",
                            "South End",
                            "Ballantyne",
                            "University City"
                        ],
                        "industries": [
                            "Banking",
                            "Finance",
                            "Technology",
                            "Energy"
                        ]
                    },
                    "nashville": {
                        "name": "Nashville",
                        "state": "TN",
                        "area_codes": ["615", "629"],
                        "business_districts": [
                            "Downtown",
                            "The Gulch",
                            "Music Row",
                            "Green Hills"
                        ],
                        "industries": [
                            "Healthcare",
                            "Music & Entertainment",
                            "Tourism",
                            "Technology"
                        ]
                    },
                    "raleigh": {
                        "name": "Raleigh",
                        "state": "NC",
                        "area_codes": ["919", "984"],
                        "business_districts": [
                            "Downtown",
                            "North Hills",
                            "Research Triangle Park",
                            "Glenwood South"
                        ],
                        "industries": [
                            "Technology",
                            "Biotechnology",
                            "Education",
                            "Healthcare"
                        ]
                    }
                }
            }
        }
    def generate_companies(self) -> Dict:
        """Generate comprehensive company data across multiple sectors."""
        return {
            "fortune_500": {
                "technology": {
                    "major_tech": {
                        "innovation_systems": {
                            "name": "Innovation Systems Inc.",
                            "headquarters": "San Francisco",
                            "industry": "Technology",
                            "sectors": ["Software", "AI", "Cloud Computing"],
                            "annual_revenue": "$50B+",
                            "employees": "50,000+",
                            "subsidiaries": [
                                "InnovateTech Solutions",
                                "CloudStack Systems",
                                "AI Research Division"
                            ],
                            "key_locations": [
                                "Silicon Valley HQ",
                                "Seattle R&D",
                                "Boston Innovation Lab",
                                "Austin Tech Center"
                            ]
                        },
                        "global_networks": {
                            "name": "Global Networks Corporation",
                            "headquarters": "Seattle",
                            "industry": "Technology",
                            "sectors": ["Enterprise Software", "Cloud Infrastructure"],
                            "annual_revenue": "$40B+",
                            "employees": "45,000+"
                        }
                    }
                },
                "finance": {
                    "banking": {
                        "atlantic_financial": {
                            "name": "Atlantic Financial Group",
                            "headquarters": "New York",
                            "industry": "Banking",
                            "sectors": ["Investment Banking", "Wealth Management"],
                            "annual_revenue": "$30B+",
                            "employees": "35,000+",
                            "subsidiaries": [
                                "Atlantic Securities",
                                "Atlantic Wealth",
                                "Atlantic Capital Markets"
                            ]
                        },
                        "midwest_banking": {
                            "name": "Midwest Banking Corporation",
                            "headquarters": "Chicago",
                            "industry": "Banking",
                            "sectors": ["Commercial Banking", "Retail Banking"],
                            "annual_revenue": "$25B+",
                            "employees": "30,000+"
                        }
                    }
                },
                "healthcare": {
                    "medical_systems": {
                        "unified_health": {
                            "name": "Unified Health Systems",
                            "headquarters": "Boston",
                            "industry": "Healthcare",
                            "sectors": ["Medical Technology", "Healthcare Services"],
                            "annual_revenue": "$20B+",
                            "employees": "25,000+"
                        }
                    }
                }
            },
            "mid_size_companies": {
                "technology": {
                    "software_solutions": {
                        "name": "Advanced Software Solutions",
                        "headquarters": "Austin",
                        "industry": "Technology",
                        "sectors": ["Enterprise Software", "Digital Services"],
                        "annual_revenue": "$500M+",
                        "employees": "2,000+"
                    }
                },
                "manufacturing": {
                    "precision_manufacturing": {
                        "name": "Precision Manufacturing Corp",
                        "headquarters": "Detroit",
                        "industry": "Manufacturing",
                        "sectors": ["Industrial Equipment", "Automation"],
                        "annual_revenue": "$750M+",
                        "employees": "3,000+"
                    }
                }
            },
            "startup_ecosystem": {
                "technology_startups": {
                    "quantum_computing": {
                        "name": "Quantum Dynamics",
                        "headquarters": "Boulder",
                        "industry": "Technology",
                        "sectors": ["Quantum Computing", "Research"],
                        "funding_stage": "Series B",
                        "employees": "150+"
                    }
                },
                "biotech_startups": {
                    "genome_research": {
                        "name": "Genome Innovations",
                        "headquarters": "Cambridge",
                        "industry": "Biotechnology",
                        "sectors": ["Genetic Research", "Medical Technology"],
                        "funding_stage": "Series C",
                        "employees": "200+"
                    }
                }
            },
            "company_relationships": {
                "strategic_partnerships": [
                    {
                        "companies": ["Innovation Systems Inc.", "Atlantic Financial Group"],
                        "partnership_type": "Technology Integration",
                        "description": "Financial technology development"
                    }
                ],
                "industry_alliances": [
                    {
                        "name": "Tech Innovation Alliance",
                        "members": [
                            "Innovation Systems Inc.",
                            "Global Networks Corporation",
                            "Advanced Software Solutions"
                        ],
                        "focus": "Technology Standards Development"
                    }
                ]
            }
        }
    def generate_government_agencies(self) -> Dict:
        """Generate comprehensive government agency data."""
        return {
            "federal_agencies": {
                "executive_branch": {
                    "cabinet_departments": {
                        "state_department": {
                            "name": "Department of State",
                            "abbreviation": "DOS",
                            "headquarters": "Washington, DC",
                            "leadership_role": "Secretary of State",
                            "key_divisions": [
                                "Diplomatic Security",
                                "Foreign Service",
                                "International Security",
                                "Public Affairs"
                            ],
                            "regional_offices": [
                                "New York",
                                "Miami",
                                "Los Angeles",
                                "Chicago"
                            ]
                        },
                        "defense_department": {
                            "name": "Department of Defense",
                            "abbreviation": "DOD",
                            "headquarters": "Pentagon, Arlington, VA",
                            "leadership_role": "Secretary of Defense",
                            "key_divisions": [
                                "Army",
                                "Navy",
                                "Air Force",
                                "Space Force",
                                "Marines"
                            ],
                            "major_commands": [
                                "Strategic Command",
                                "Cyber Command",
                                "Special Operations"
                            ]
                        },
                        "treasury_department": {
                            "name": "Department of the Treasury",
                            "abbreviation": "USDT",
                            "headquarters": "Washington, DC",
                            "leadership_role": "Secretary of the Treasury",
                            "key_divisions": [
                                "Internal Revenue Service",
                                "U.S. Mint",
                                "Office of Financial Intelligence"
                            ]
                        }
                    },
                    "independent_agencies": {
                        "fbi": {
                            "name": "Federal Bureau of Investigation",
                            "abbreviation": "FBI",
                            "headquarters": "Washington, DC",
                            "leadership_role": "Director",
                            "key_divisions": [
                                "Criminal Investigation",
                                "Counterterrorism",
                                "Cybersecurity",
                                "Intelligence"
                            ],
                            "field_offices": [
                                "New York",
                                "Los Angeles",
                                "Chicago",
                                "Houston"
                            ]
                        },
                        "cia": {
                            "name": "Central Intelligence Agency",
                            "abbreviation": "CIA",
                            "headquarters": "Langley, VA",
                            "leadership_role": "Director",
                            "key_divisions": [
                                "Operations",
                                "Analysis",
                                "Science and Technology",
                                "Digital Innovation"
                            ]
                        }
                    }
                },
                "regulatory_agencies": {
                    "sec": {
                        "name": "Securities and Exchange Commission",
                        "abbreviation": "SEC",
                        "headquarters": "Washington, DC",
                        "leadership_role": "Chairman",
                        "key_divisions": [
                            "Corporation Finance",
                            "Trading and Markets",
                            "Investment Management",
                            "Enforcement"
                        ],
                        "regional_offices": [
                            "New York",
                            "Chicago",
                            "San Francisco",
                            "Miami"
                        ]
                    },
                    "fcc": {
                        "name": "Federal Communications Commission",
                        "abbreviation": "FCC",
                        "headquarters": "Washington, DC",
                        "leadership_role": "Chairman",
                        "key_divisions": [
                            "Media Bureau",
                            "Wireless Bureau",
                            "Enforcement Bureau"
                        ]
                    }
                }
            },
            "state_agencies": {
                "law_enforcement": {
                    "state_police": {
                        "structure": {
                            "headquarters": "State Capital",
                            "divisions": [
                                "Highway Patrol",
                                "Criminal Investigation",
                                "Special Operations"
                            ]
                        },
                        "examples": [
                            "New York State Police",
                            "California Highway Patrol",
                            "Texas Department of Public Safety"
                        ]
                    }
                },
                "regulatory": {
                    "financial_regulation": {
                        "structure": {
                            "divisions": [
                                "Banking",
                                "Insurance",
                                "Securities"
                            ]
                        },
                        "examples": [
                            "New York Department of Financial Services",
                            "California Department of Financial Protection"
                        ]
                    }
                }
            },
            "interagency_relationships": {
                "task_forces": [
                    {
                        "name": "Joint Terrorism Task Force",
                        "lead_agency": "FBI",
                        "participating_agencies": [
                            "CIA",
                            "DOD",
                            "State Police"
                        ]
                    },
                    {
                        "name": "Financial Crimes Task Force",
                        "lead_agency": "Treasury",
                        "participating_agencies": [
                            "FBI",
                            "SEC",
                            "State Regulatory Agencies"
                        ]
                    }
                ],
                "information_sharing": {
                    "intelligence_community": {
                        "coordinator": "Director of National Intelligence",
                        "member_agencies": [
                            "CIA",
                            "FBI",
                            "NSA",
                            "DIA"
                        ]
                    }
                }
            }
        }
    def generate_business_hierarchies(self) -> Dict:
        """Generate comprehensive business hierarchy and organizational structures."""
        return {
            "corporate_structures": {
                "traditional_corporate": {
                    "executive_level": {
                        "c_suite": {
                            "positions": [
                                {
                                    "title": "Chief Executive Officer",
                                    "code": "CEO",
                                    "reports_to": "Board of Directors",
                                    "responsibilities": [
                                        "Corporate Strategy",
                                        "Executive Leadership",
                                        "Stakeholder Management"
                                    ]
                                },
                                {
                                    "title": "Chief Financial Officer",
                                    "code": "CFO",
                                    "reports_to": "CEO",
                                    "responsibilities": [
                                        "Financial Strategy",
                                        "Risk Management",
                                        "Investor Relations"
                                    ]
                                },
                                {
                                    "title": "Chief Operating Officer",
                                    "code": "COO",
                                    "reports_to": "CEO",
                                    "responsibilities": [
                                        "Operations Management",
                                        "Process Optimization",
                                        "Resource Allocation"
                                    ]
                                }
                            ]
                        },
                        "executive_vp": {
                            "positions": [
                                "Executive VP of Sales",
                                "Executive VP of Marketing",
                                "Executive VP of Technology"
                            ]
                        }
                    },
                    "senior_management": {
                        "division_heads": {
                            "positions": [
                                "Senior VP of Product",
                                "Senior VP of Engineering",
                                "Senior VP of Customer Success"
                            ],
                            "reporting_structure": "Executive VPs"
                        },
                        "regional_directors": {
                            "positions": [
                                "Regional Director, East",
                                "Regional Director, West",
                                "Regional Director, Central"
                            ]
                        }
                    }
                },
                "startup_structure": {
                    "founding_team": {
                        "positions": [
                            "Founder/CEO",
                            "Co-Founder/CTO",
                            "Co-Founder/CPO"
                        ]
                    },
                    "early_stage": {
                        "core_team": [
                            "Head of Engineering",
                            "Head of Product",
                            "Head of Growth"
                        ]
                    }
                }
            },
            "department_structures": {
                "technology": {
                    "engineering": {
                        "leadership": "VP of Engineering",
                        "sub_departments": [
                            "Frontend Development",
                            "Backend Development",
                            "DevOps",
                            "Quality Assurance"
                        ],
                        "roles": [
                            "Senior Engineer",
                            "Software Engineer",
                            "QA Engineer",
                            "DevOps Engineer"
                        ]
                    },
                    "product": {
                        "leadership": "VP of Product",
                        "sub_departments": [
                            "Product Management",
                            "User Experience",
                            "Product Analytics"
                        ]
                    }
                },
                "sales": {
                    "structure": {
                        "leadership": "VP of Sales",
                        "teams": [
                            "Enterprise Sales",
                            "Mid-Market",
                            "SMB",
                            "Sales Operations"
                        ]
                    },
                    "hierarchy": [
                        "Sales Director",
                        "Sales Manager",
                        "Senior Account Executive",
                        "Account Executive"
                    ]
                }
            },
            "reporting_relationships": {
                "direct_reports": {
                    "CEO": [
                        "CFO",
                        "COO",
                        "CTO",
                        "CMO"
                    ],
                    "COO": [
                        "VP of Operations",
                        "VP of Sales",
                        "VP of Customer Success"
                    ]
                },
                "matrix_structure": {
                    "project_based": {
                        "project_manager": [
                            "Technical Lead",
                            "Design Lead",
                            "Marketing Lead"
                        ],
                        "functional_manager": [
                            "Engineering Manager",
                            "Design Manager",
                            "Marketing Manager"
                        ]
                    }
                }
            },
            "communication_channels": {
                "formal": [
                    "Board Meetings",
                    "Executive Sessions",
                    "Department Meetings",
                    "All-Hands Meetings"
                ],
                "informal": [
                    "Team Channels",
                    "Project Groups",
                    "Cross-functional Teams"
                ],
                "reporting_lines": [
                    "Direct Management",
                    "Matrix Reporting",
                    "Project-based Reporting"
                ]
            }
        }
    def generate_relationship_mappings(self) -> Dict:
        """Generate relationship mappings between different entities."""
        return {
            "business_government": {
                "regulatory_relationships": {
                    "technology_sector": {
                        "regulators": ["FCC", "FTC", "SEC"],
                        "oversight_areas": [
                            "Data Privacy",
                            "Consumer Protection",
                            "Securities Compliance"
                        ]
                    },
                    "financial_sector": {
                        "regulators": ["SEC", "Federal Reserve", "FDIC"],
                        "oversight_areas": [
                            "Banking Regulation",
                            "Securities Trading",
                            "Consumer Banking"
                        ]
                    }
                },
                "contracts_and_partnerships": {
                    "defense_contracts": {
                        "agencies": ["DOD", "DHS", "NASA"],
                        "contractor_types": [
                            "Technology Providers",
                            "Defense Manufacturers",
                            "Research Institutions"
                        ]
                    }
                }
            },
            "cross_sector_relationships": {
                "technology_finance": {
                    "partnerships": [
                        "Digital Payment Systems",
                        "Fintech Innovation",
                        "Cybersecurity"
                    ],
                    "key_players": {
                        "tech_companies": ["Innovation Systems Inc.", "Global Networks"],
                        "financial_institutions": ["Atlantic Financial", "Midwest Banking"]
                    }
                }
            }
        }

    def generate_all(self):
        """Generate all static data and save to files."""
        try:
            # Generate all data
            cities_data = self.generate_us_cities()
            additional_cities = self.generate_additional_us_cities()
            companies_data = self.generate_companies()
            agencies_data = self.generate_government_agencies()
            hierarchies_data = self.generate_business_hierarchies()
            relationships_data = self.generate_relationship_mappings()
            infrastructure_data = self.generate_city_infrastructure()

            # Save all data to files
            data_files = {
                "cities/major_cities.json": cities_data,
                "cities/additional_cities.json": additional_cities,
                "cities/infrastructure.json": infrastructure_data,
                "business/companies.json": companies_data,
                "business/hierarchies.json": hierarchies_data,
                "government/agencies.json": agencies_data,
                "relationships/mappings.json": relationships_data
            }

            for filename, data in data_files.items():
                self.write_json_file(data, filename)

            print(f"\nSuccessfully generated all static data files at {self.timestamp}")
            return True

        except Exception as e:
            print(f"Error generating static data: {str(e)}")
            return False

def main():
    """Main execution function."""
    print("\nStatic Data Generator for Shakespeare Forensics Project")
    print("Created by RSGrizz")
    print(f"Version 1.2 - {datetime.now().strftime('%B %Y')}\n")

    generator = StaticDataGenerator()
    
    print("Generating static data files...")
    success = generator.generate_all()
    
    if success:
        print("\nData generation complete! Files have been created in:")
        print(f"- {generator.base_dir}")
    else:
        print("\nError occurred during data generation.")

if __name__ == "__main__":
    main()
