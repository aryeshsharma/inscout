import csv
import io
from typing import List
from app.models.profile import DiscoveredProfile

class Exporter:
    
    @staticmethod
    def export_to_csv(profiles: List[DiscoveredProfile]) -> str:
        output = io.StringIO()
        writer = csv.writer(output, quoting=csv.QUOTE_MINIMAL)
        
        # Standard RFC4180 CSV Header
        writer.writerow([
            "Username",
            "Profile URL",
            "Display Name",
            "Followers",
            "Region",
            "Tags",
            "Match Score",
            "Match Reasons",
            "Data Confidence",
            "Discovery Source"
        ])
        
        for p in profiles:
            reasons_text = "; ".join([r.description for r in p.match_reasons if r.matched])
            tags_text = ", ".join(p.tags) if p.tags else "None"
            followers_text = str(p.followers) if p.followers is not None else "Not available"
            region_text = p.region if p.region else "Not available"
            display_name_text = p.display_name if p.display_name else "Not available"
            
            writer.writerow([
                f"@{p.username}",
                p.profile_url,
                display_name_text,
                followers_text,
                region_text,
                tags_text,
                p.match_score,
                reasons_text,
                p.data_confidence.value,
                "Public Web Discovery"
            ])
            
        return output.getvalue()
