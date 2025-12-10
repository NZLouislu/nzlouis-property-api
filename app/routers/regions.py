from fastapi import APIRouter, HTTPException
from typing import List
from app.models.region import Region, City, Suburb

router = APIRouter(prefix="/regions", tags=["Regions"])

REGIONS_DATA: List[Region] = [
    Region(
        id="wellington",
        name="Wellington",
        cities=[
            City(
                id="wellington-city",
                name="Wellington City",
                suburbs=[
                    Suburb(id="aro valley", name="Aro Valley"),
                    Suburb(id="berhampore", name="Berhampore"),
                    Suburb(id="brooklyn", name="Brooklyn"),
                    Suburb(id="hataitai", name="Hataitai"),
                    Suburb(id="island bay", name="Island Bay"),
                    Suburb(id="karori", name="Karori"),
                    Suburb(id="kelburn", name="Kelburn"),
                    Suburb(id="kilbirnie", name="Kilbirnie"),
                    Suburb(id="lyall bay", name="Lyall Bay"),
                    Suburb(id="miramar", name="Miramar"),
                    Suburb(id="mount cook", name="Mount Cook"),
                    Suburb(id="mount victoria", name="Mount Victoria"),
                    Suburb(id="newtown", name="Newtown"),
                    Suburb(id="northland", name="Northland"),
                    Suburb(id="oriental bay", name="Oriental Bay"),
                    Suburb(id="roseneath", name="Roseneath"),
                    Suburb(id="seatoun", name="Seatoun"),
                    Suburb(id="southgate", name="Southgate"),
                    Suburb(id="strathmore park", name="Strathmore Park"),
                    Suburb(id="te aro", name="Te Aro"),
                    Suburb(id="thorndon", name="Thorndon"),
                    Suburb(id="wadestown", name="Wadestown"),
                    Suburb(id="wellington central", name="Wellington Central"),
                ]
            ),
            City(
                id="lower-hutt",
                name="Lower Hutt",
                suburbs=[
                    Suburb(id="alicetown", name="Alicetown"),
                    Suburb(id="avalon", name="Avalon"),
                    Suburb(id="belmont", name="Belmont"),
                    Suburb(id="epuni", name="Epuni"),
                    Suburb(id="gracefield", name="Gracefield"),
                    Suburb(id="korokoro", name="Korokoro"),
                    Suburb(id="manor park", name="Manor Park"),
                    Suburb(id="moera", name="Moera"),
                    Suburb(id="naenae", name="Naenae"),
                    Suburb(id="normandale", name="Normandale"),
                    Suburb(id="petone", name="Petone"),
                    Suburb(id="seaview", name="Seaview"),
                    Suburb(id="stokes valley", name="Stokes Valley"),
                    Suburb(id="taita", name="Taita"),
                    Suburb(id="wainuiomata", name="Wainuiomata"),
                    Suburb(id="waterloo", name="Waterloo"),
                ]
            ),
            City(
                id="upper-hutt",
                name="Upper Hutt",
                suburbs=[
                    Suburb(id="akatarawa", name="Akatarawa"),
                    Suburb(id="birchville", name="Birchville"),
                    Suburb(id="brown owl", name="Brown Owl"),
                    Suburb(id="ebdentown", name="Ebdentown"),
                    Suburb(id="heretaunga", name="Heretaunga"),
                    Suburb(id="maoribank", name="Maoribank"),
                    Suburb(id="pinehaven", name="Pinehaven"),
                    Suburb(id="silverstream", name="Silverstream"),
                    Suburb(id="trentham", name="Trentham"),
                    Suburb(id="wallaceville", name="Wallaceville"),
                ]
            ),
            City(
                id="porirua",
                name="Porirua",
                suburbs=[
                    Suburb(id="ascot park", name="Ascot Park"),
                    Suburb(id="cannons creek", name="Cannons Creek"),
                    Suburb(id="elsdon", name="Elsdon"),
                    Suburb(id="papakowhai", name="Papakowhai"),
                    Suburb(id="paremata", name="Paremata"),
                    Suburb(id="plimmerton", name="Plimmerton"),
                    Suburb(id="porirua central", name="Porirua Central"),
                    Suburb(id="pukerua bay", name="Pukerua Bay"),
                    Suburb(id="ranui heights", name="Ranui Heights"),
                    Suburb(id="titahi bay", name="Titahi Bay"),
                    Suburb(id="waitangirua", name="Waitangirua"),
                    Suburb(id="whitby", name="Whitby"),
                ]
            ),
        ]
    ),
    Region(
        id="auckland",
        name="Auckland",
        cities=[
            City(
                id="auckland-city",
                name="Auckland - City",
                suburbs=[
                    Suburb(id="auckland central", name="Auckland Central"),
                    Suburb(id="grafton", name="Grafton"),
                    Suburb(id="grey lynn", name="Grey Lynn"),
                    Suburb(id="herne bay", name="Herne Bay"),
                    Suburb(id="kingsland", name="Kingsland"),
                    Suburb(id="mount eden", name="Mount Eden"),
                    Suburb(id="newton", name="Newton"),
                    Suburb(id="parnell", name="Parnell"),
                    Suburb(id="ponsonby", name="Ponsonby"),
                    Suburb(id="remuera", name="Remuera"),
                    Suburb(id="westmere", name="Westmere"),
                ]
            ),
            City(
                id="north-shore",
                name="Auckland - North Shore",
                suburbs=[
                    Suburb(id="albany", name="Albany"),
                    Suburb(id="bayswater", name="Bayswater"),
                    Suburb(id="belmont", name="Belmont"),
                    Suburb(id="birkenhead", name="Birkenhead"),
                    Suburb(id="browns bay", name="Browns Bay"),
                    Suburb(id="campbells bay", name="Campbells Bay"),
                    Suburb(id="castor bay", name="Castor Bay"),
                    Suburb(id="devonport", name="Devonport"),
                    Suburb(id="forrest hill", name="Forrest Hill"),
                    Suburb(id="glenfield", name="Glenfield"),
                    Suburb(id="mairangi bay", name="Mairangi Bay"),
                    Suburb(id="milford", name="Milford"),
                    Suburb(id="northcote", name="Northcote"),
                    Suburb(id="rothesay bay", name="Rothesay Bay"),
                    Suburb(id="takapuna", name="Takapuna"),
                    Suburb(id="torbay", name="Torbay"),
                ]
            ),
            City(
                id="manukau",
                name="Auckland - Manukau",
                suburbs=[
                    Suburb(id="botany downs", name="Botany Downs"),
                    Suburb(id="east tamaki", name="East Tamaki"),
                    Suburb(id="flat bush", name="Flat Bush"),
                    Suburb(id="howick", name="Howick"),
                    Suburb(id="manukau central", name="Manukau Central"),
                    Suburb(id="manurewa", name="Manurewa"),
                    Suburb(id="otara", name="Otara"),
                    Suburb(id="pakuranga", name="Pakuranga"),
                    Suburb(id="papakura", name="Papakura"),
                ]
            ),
            City(
                id="waitakere",
                name="Auckland - Waitakere",
                suburbs=[
                    Suburb(id="glen eden", name="Glen Eden"),
                    Suburb(id="henderson", name="Henderson"),
                    Suburb(id="massey", name="Massey"),
                    Suburb(id="new lynn", name="New Lynn"),
                    Suburb(id="ranui", name="Ranui"),
                    Suburb(id="swanson", name="Swanson"),
                    Suburb(id="te atatu", name="Te Atatu"),
                    Suburb(id="titirangi", name="Titirangi"),
                    Suburb(id="west harbour", name="West Harbour"),
                ]
            ),
        ]
    ),
]

@router.get("", response_model=List[Region])
async def get_regions() -> List[Region]:
    try:
        return REGIONS_DATA
    except Exception as e:
        raise HTTPException(status_code=500, detail="Failed to fetch regions")
