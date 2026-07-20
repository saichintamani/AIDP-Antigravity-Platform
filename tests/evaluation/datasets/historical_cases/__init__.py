from .case_crispr import case_data as case_crispr
from .case_gravitational_waves import case_data as case_gravitational_waves
from .case_h_pylori import case_data as case_h_pylori
from .case_helicase import case_data as case_helicase
from .case_ht_superconductors import case_data as case_ht_superconductors
from .case_mrna_lnp import case_data as case_mrna_lnp
from .case_plate_tectonics import case_data as case_plate_tectonics
from .case_prions import case_data as case_prions
from .case_quasicrystals import case_data as case_quasicrystals
from .case_rnai import case_data as case_rnai

ALL_CASES = [
    case_crispr,
    case_plate_tectonics,
    case_h_pylori,
    case_prions,
    case_quasicrystals,
    case_ht_superconductors,
    case_rnai,
    case_mrna_lnp,
    case_helicase,
    case_gravitational_waves
]
