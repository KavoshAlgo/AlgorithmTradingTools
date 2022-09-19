class AccountInfo:
    USERNAME = "username"
    EMAIL = "email"
    PORTFOLIO_MAPPING = "portfolio_mapping"  # mapping for portfolio matrix indices
    PORTFOLIO_MATRIX_SHAPE = "portfolio_matrix_shape"  # shape of portfolio matrix
    PORTFOLIO_SHM_NAME = "portfolio_shm_name"  # shape of portfolio matrix

    class CommissionMode:
        MAKER = 'maker'  # COMMISSION FEE OF MAKER TRADES
        TAKER = 'taker'  # COMMISSION FEE OF TAKER TRADES
