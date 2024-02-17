from solana_jup.unit_buy_price import save_unit_buy_price

if __name__ == '__main__':
    base = "SOL"
    quote = "USDC"
    measurement_name = "unit_buy_price3"
    bucket_name = "test_bucket"
    save_unit_buy_price(base, quote, measurement_name, bucket_name)
