class AccountInfo:
    USERNAME = "username"
    EMAIL = "email"
    PORTFOLIO_MAPPING = "portfolio_mapping"  # mapping for portfolio matrix indices
    PORTFOLIO_MATRIX_SHAPE = "portfolio_matrix_shape"  # shape of portfolio matrix
    PORTFOLIO_SHM_NAME = "portfolio_shm_name"  # shape of portfolio matrix
    ORDERS_MATRIX_SHAPE = "orders_matrix_shape"  # shape of portfolio matrix
    ORDERS_SHM_NAME = "orders_shm_name"  # shape of portfolio matrix
    API_TOKEN = "api_token"  # the api token of this account

    class CommissionMode:
        MAKER = 'maker'  # COMMISSION FEE OF MAKER TRADES
        TAKER = 'taker'  # COMMISSION FEE OF TAKER TRADES
