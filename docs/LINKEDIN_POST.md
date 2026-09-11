I wanted to learn more about the data-engineering challenges behind robotics AI systems, so I built a small proof-of-concept around one problem:

**How do we stop poor-quality multimodal sensor data from silently reaching a downstream training dataset?**

I built a pipeline that:

→ ingests raw sensor events  
→ validates required fields and numeric values  
→ detects duplicate events  
→ checks sensor ranges  
→ separates accepted and rejected records  
→ records the reason for every rejection  
→ produces a curated dataset and quality report

For the sample dataset:

**25 raw records → 21 accepted + 4 rejected**

Tech: Python | PySpark | ETL | Data Quality | Azure architecture

I intentionally focused on the Data Engineering layer because it closely matches the work I already do, rather than trying to reproduce a robotics or ML system.

Case study + code:
[PASTE GITHUB LINK]

I found the data infrastructure problem at @Intelligence Factory particularly interesting, so I built this POC to explore the problem hands-on.

#DataEngineering #PySpark #Python #DataQuality #ETL #Robotics #DataInfrastructure
