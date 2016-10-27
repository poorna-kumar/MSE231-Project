make_index.py:
    makes the index given a year for all fields in the NYT Corpus

index:
    a tab delineated file to index articles where each article has only one value
    see index.header for the headers
    Guid - unique identifier of the article

index_m:
    a tabl delineated file to index articles where each article may have more than one value
    see index_m.header for the headers
    Guid - unique identifier of the article
    Tag - name of the tag of the interest
    Tag_Type - type of tag:
        0   Online_People
        1   Online_Locations
        2   Online_Descriptors
        3   Names
        4   General_Online_Descriptors
        5   Descriptors
        6   Taxonomic_Classifiers
        7   People
        8   Locations
        9   Online_Sections

