# -----------------------------------------------------------------------------
# Basic Function To Test
# -----------------------------------------------------------------------------

def l4_011CalculateTransactionFee(
        amount: float,
        fee_percentage: float,
) -> float:
    """Calculate transaction fee."""

    # Calculate transaction fee.
    transaction_fee = amount * fee_percentage / 100

    return transaction_fee

# -----------------------------------------------------------------------------
# Test Transaction Fee Calculation
# -----------------------------------------------------------------------------

def test_l4_011CalculateTransactionFee() -> None:
    """Test transaction fee calculation."""

    # Call function with test values.
    result = l4_011CalculateTransactionFee(
        amount = 1000,
        fee_percentage = 2,
    )

    # verify expected result
    assert result == 20

# -----------------------------------------------------------------------------
# Test Zero Transaction Fee
# -----------------------------------------------------------------------------

def test_l4_011ZeroTransactionFee() -> None:
    """Test transaction with zero fee."""

    # Call function with zero fee.
    result = l4_011CalculateTransactionFee(
        amount = 1000,
        fee_percentage = 0
    )

    # verify expected result
    assert result == 0

# -----------------------------------------------------------------------------
# Test Zero Amount fee
# -----------------------------------------------------------------------------

def test_l4_011ZeroAmount() -> None:
    """Test transaction with zero amount."""

    # call function with zero amount value
    result = l4_011CalculateTransactionFee(
        amount = 0,
        fee_percentage = 1
    )

    # verify expected result
    assert result == 0
