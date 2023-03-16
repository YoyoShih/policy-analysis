from api.mortality_rate import read, create, delete

"""
取得 mortality-rate 列表
mortality_rate_id 為 list_mortality_rates
"""
print('mortality-rate-get', read(6))

"""
建立新的 mortality-rate 

"""
data = {
    "name": "2021 TSO TEST",
    "data": [
        {
            "gender": 1,
            "age": 0,
            "value": "0.0003200000"
        },
        {
            "gender": 1,
            "age": 1,
            "value": "0.0001890000"
        },
        {
            "gender": 1,
            "age": 2,
            "value": "0.0001630000"
        },
        {
            "gender": 1,
            "age": 3,
            "value": "0.0001400000"
        },
        {
            "gender": 1,
            "age": 4,
            "value": "0.0001250000"
        },
        {
            "gender": 1,
            "age": 5,
            "value": "0.0001140000"
        },
        {
            "gender": 1,
            "age": 6,
            "value": "0.0001110000"
        },
        {
            "gender": 1,
            "age": 7,
            "value": "0.0001120000"
        },
        {
            "gender": 1,
            "age": 8,
            "value": "0.0001140000"
        },
        {
            "gender": 1,
            "age": 9,
            "value": "0.0001190000"
        },
        {
            "gender": 1,
            "age": 10,
            "value": "0.0001220000"
        },
        {
            "gender": 1,
            "age": 11,
            "value": "0.0001370000"
        },
        {
            "gender": 1,
            "age": 12,
            "value": "0.0001550000"
        },
        {
            "gender": 1,
            "age": 13,
            "value": "0.0001810000"
        },
        {
            "gender": 1,
            "age": 14,
            "value": "0.0002270000"
        },
        {
            "gender": 1,
            "age": 15,
            "value": "0.0002960000"
        },
        {
            "gender": 1,
            "age": 16,
            "value": "0.0003390000"
        },
        {
            "gender": 1,
            "age": 17,
            "value": "0.0003780000"
        },
        {
            "gender": 1,
            "age": 18,
            "value": "0.0004100000"
        },
        {
            "gender": 1,
            "age": 19,
            "value": "0.0004350000"
        },
        {
            "gender": 1,
            "age": 20,
            "value": "0.0004320000"
        },
        {
            "gender": 1,
            "age": 21,
            "value": "0.0004470000"
        },
        {
            "gender": 1,
            "age": 22,
            "value": "0.0004590000"
        },
        {
            "gender": 1,
            "age": 23,
            "value": "0.0004660000"
        },
        {
            "gender": 1,
            "age": 24,
            "value": "0.0004720000"
        },
        {
            "gender": 1,
            "age": 25,
            "value": "0.0004960000"
        },
        {
            "gender": 1,
            "age": 26,
            "value": "0.0005040000"
        },
        {
            "gender": 1,
            "age": 27,
            "value": "0.0005180000"
        },
        {
            "gender": 1,
            "age": 28,
            "value": "0.0005380000"
        },
        {
            "gender": 1,
            "age": 29,
            "value": "0.0005650000"
        },
        {
            "gender": 1,
            "age": 30,
            "value": "0.0006570000"
        },
        {
            "gender": 1,
            "age": 31,
            "value": "0.0006980000"
        },
        {
            "gender": 1,
            "age": 32,
            "value": "0.0007490000"
        },
        {
            "gender": 1,
            "age": 33,
            "value": "0.0008080000"
        },
        {
            "gender": 1,
            "age": 34,
            "value": "0.0008770000"
        },
        {
            "gender": 1,
            "age": 35,
            "value": "0.0009770000"
        },
        {
            "gender": 1,
            "age": 36,
            "value": "0.0010630000"
        },
        {
            "gender": 1,
            "age": 37,
            "value": "0.0011600000"
        },
        {
            "gender": 1,
            "age": 38,
            "value": "0.0012680000"
        },
        {
            "gender": 1,
            "age": 39,
            "value": "0.0013860000"
        },
        {
            "gender": 1,
            "age": 40,
            "value": "0.0015280000"
        },
        {
            "gender": 1,
            "age": 41,
            "value": "0.0016660000"
        },
        {
            "gender": 1,
            "age": 42,
            "value": "0.0018130000"
        },
        {
            "gender": 1,
            "age": 43,
            "value": "0.0019720000"
        },
        {
            "gender": 1,
            "age": 44,
            "value": "0.0021410000"
        },
        {
            "gender": 1,
            "age": 45,
            "value": "0.0024170000"
        },
        {
            "gender": 1,
            "age": 46,
            "value": "0.0026070000"
        },
        {
            "gender": 1,
            "age": 47,
            "value": "0.0028090000"
        },
        {
            "gender": 1,
            "age": 48,
            "value": "0.0030230000"
        },
        {
            "gender": 1,
            "age": 49,
            "value": "0.0032500000"
        },
        {
            "gender": 1,
            "age": 50,
            "value": "0.0034620000"
        },
        {
            "gender": 1,
            "age": 51,
            "value": "0.0037160000"
        },
        {
            "gender": 1,
            "age": 52,
            "value": "0.0039870000"
        },
        {
            "gender": 1,
            "age": 53,
            "value": "0.0042760000"
        },
        {
            "gender": 1,
            "age": 54,
            "value": "0.0045850000"
        },
        {
            "gender": 1,
            "age": 55,
            "value": "0.0050600000"
        },
        {
            "gender": 1,
            "age": 56,
            "value": "0.0054160000"
        },
        {
            "gender": 1,
            "age": 57,
            "value": "0.0058020000"
        },
        {
            "gender": 1,
            "age": 58,
            "value": "0.0062220000"
        },
        {
            "gender": 1,
            "age": 59,
            "value": "0.0066780000"
        },
        {
            "gender": 1,
            "age": 60,
            "value": "0.0074610000"
        },
        {
            "gender": 1,
            "age": 61,
            "value": "0.0080050000"
        },
        {
            "gender": 1,
            "age": 62,
            "value": "0.0086100000"
        },
        {
            "gender": 1,
            "age": 63,
            "value": "0.0092830000"
        },
        {
            "gender": 1,
            "age": 64,
            "value": "0.0100400000"
        },
        {
            "gender": 1,
            "age": 65,
            "value": "0.0112630000"
        },
        {
            "gender": 1,
            "age": 66,
            "value": "0.0122330000"
        },
        {
            "gender": 1,
            "age": 67,
            "value": "0.0133470000"
        },
        {
            "gender": 1,
            "age": 68,
            "value": "0.0146130000"
        },
        {
            "gender": 1,
            "age": 69,
            "value": "0.0160340000"
        },
        {
            "gender": 1,
            "age": 70,
            "value": "0.0185080000"
        },
        {
            "gender": 1,
            "age": 71,
            "value": "0.0202260000"
        },
        {
            "gender": 1,
            "age": 72,
            "value": "0.0221100000"
        },
        {
            "gender": 1,
            "age": 73,
            "value": "0.0241670000"
        },
        {
            "gender": 1,
            "age": 74,
            "value": "0.0264210000"
        },
        {
            "gender": 1,
            "age": 75,
            "value": "0.0286840000"
        },
        {
            "gender": 1,
            "age": 76,
            "value": "0.0313990000"
        },
        {
            "gender": 1,
            "age": 77,
            "value": "0.0343930000"
        },
        {
            "gender": 1,
            "age": 78,
            "value": "0.0376860000"
        },
        {
            "gender": 1,
            "age": 79,
            "value": "0.0412830000"
        },
        {
            "gender": 1,
            "age": 80,
            "value": "0.0451790000"
        },
        {
            "gender": 1,
            "age": 81,
            "value": "0.0493790000"
        },
        {
            "gender": 1,
            "age": 82,
            "value": "0.0539190000"
        },
        {
            "gender": 1,
            "age": 83,
            "value": "0.0588470000"
        },
        {
            "gender": 1,
            "age": 84,
            "value": "0.0642340000"
        },
        {
            "gender": 1,
            "age": 85,
            "value": "0.0701550000"
        },
        {
            "gender": 1,
            "age": 86,
            "value": "0.0766790000"
        },
        {
            "gender": 1,
            "age": 87,
            "value": "0.0838620000"
        },
        {
            "gender": 1,
            "age": 88,
            "value": "0.0915030000"
        },
        {
            "gender": 1,
            "age": 89,
            "value": "0.0995530000"
        },
        {
            "gender": 1,
            "age": 90,
            "value": "0.1088140000"
        },
        {
            "gender": 1,
            "age": 91,
            "value": "0.1195220000"
        },
        {
            "gender": 1,
            "age": 92,
            "value": "0.1301400000"
        },
        {
            "gender": 1,
            "age": 93,
            "value": "0.1417150000"
        },
        {
            "gender": 1,
            "age": 94,
            "value": "0.1543330000"
        },
        {
            "gender": 1,
            "age": 95,
            "value": "0.1680880000"
        },
        {
            "gender": 1,
            "age": 96,
            "value": "0.1830830000"
        },
        {
            "gender": 1,
            "age": 97,
            "value": "0.1994290000"
        },
        {
            "gender": 1,
            "age": 98,
            "value": "0.2172480000"
        },
        {
            "gender": 1,
            "age": 99,
            "value": "0.2366730000"
        },
        {
            "gender": 1,
            "age": 100,
            "value": "0.2578490000"
        },
        {
            "gender": 1,
            "age": 101,
            "value": "0.2802660000"
        },
        {
            "gender": 1,
            "age": 102,
            "value": "0.3033800000"
        },
        {
            "gender": 1,
            "age": 103,
            "value": "0.3279410000"
        },
        {
            "gender": 1,
            "age": 104,
            "value": "0.3539360000"
        },
        {
            "gender": 1,
            "age": 105,
            "value": "0.3813570000"
        },
        {
            "gender": 1,
            "age": 106,
            "value": "0.4230240000"
        },
        {
            "gender": 1,
            "age": 107,
            "value": "0.4683080000"
        },
        {
            "gender": 1,
            "age": 108,
            "value": "0.5125490000"
        },
        {
            "gender": 1,
            "age": 109,
            "value": "0.5585880000"
        },
        {
            "gender": 1,
            "age": 110,
            "value": "1.0000000000"
        },
        {
            "gender": 2,
            "age": 0,
            "value": "0.0002500000"
        },
        {
            "gender": 2,
            "age": 1,
            "value": "0.0001450000"
        },
        {
            "gender": 2,
            "age": 2,
            "value": "0.0001240000"
        },
        {
            "gender": 2,
            "age": 3,
            "value": "0.0001050000"
        },
        {
            "gender": 2,
            "age": 4,
            "value": "0.0000930000"
        },
        {
            "gender": 2,
            "age": 5,
            "value": "0.0000830000"
        },
        {
            "gender": 2,
            "age": 6,
            "value": "0.0000800000"
        },
        {
            "gender": 2,
            "age": 7,
            "value": "0.0000780000"
        },
        {
            "gender": 2,
            "age": 8,
            "value": "0.0000760000"
        },
        {
            "gender": 2,
            "age": 9,
            "value": "0.0000750000"
        },
        {
            "gender": 2,
            "age": 10,
            "value": "0.0000700000"
        },
        {
            "gender": 2,
            "age": 11,
            "value": "0.0000720000"
        },
        {
            "gender": 2,
            "age": 12,
            "value": "0.0000770000"
        },
        {
            "gender": 2,
            "age": 13,
            "value": "0.0000850000"
        },
        {
            "gender": 2,
            "age": 14,
            "value": "0.0000970000"
        },
        {
            "gender": 2,
            "age": 15,
            "value": "0.0001300000"
        },
        {
            "gender": 2,
            "age": 16,
            "value": "0.0001440000"
        },
        {
            "gender": 2,
            "age": 17,
            "value": "0.0001570000"
        },
        {
            "gender": 2,
            "age": 18,
            "value": "0.0001690000"
        },
        {
            "gender": 2,
            "age": 19,
            "value": "0.0001810000"
        },
        {
            "gender": 2,
            "age": 20,
            "value": "0.0001780000"
        },
        {
            "gender": 2,
            "age": 21,
            "value": "0.0001870000"
        },
        {
            "gender": 2,
            "age": 22,
            "value": "0.0001960000"
        },
        {
            "gender": 2,
            "age": 23,
            "value": "0.0002030000"
        },
        {
            "gender": 2,
            "age": 24,
            "value": "0.0002090000"
        },
        {
            "gender": 2,
            "age": 25,
            "value": "0.0002400000"
        },
        {
            "gender": 2,
            "age": 26,
            "value": "0.0002490000"
        },
        {
            "gender": 2,
            "age": 27,
            "value": "0.0002600000"
        },
        {
            "gender": 2,
            "age": 28,
            "value": "0.0002750000"
        },
        {
            "gender": 2,
            "age": 29,
            "value": "0.0002930000"
        },
        {
            "gender": 2,
            "age": 30,
            "value": "0.0003130000"
        },
        {
            "gender": 2,
            "age": 31,
            "value": "0.0003350000"
        },
        {
            "gender": 2,
            "age": 32,
            "value": "0.0003580000"
        },
        {
            "gender": 2,
            "age": 33,
            "value": "0.0003830000"
        },
        {
            "gender": 2,
            "age": 34,
            "value": "0.0004090000"
        },
        {
            "gender": 2,
            "age": 35,
            "value": "0.0004420000"
        },
        {
            "gender": 2,
            "age": 36,
            "value": "0.0004740000"
        },
        {
            "gender": 2,
            "age": 37,
            "value": "0.0005100000"
        },
        {
            "gender": 2,
            "age": 38,
            "value": "0.0005500000"
        },
        {
            "gender": 2,
            "age": 39,
            "value": "0.0005940000"
        },
        {
            "gender": 2,
            "age": 40,
            "value": "0.0006540000"
        },
        {
            "gender": 2,
            "age": 41,
            "value": "0.0007060000"
        },
        {
            "gender": 2,
            "age": 42,
            "value": "0.0007630000"
        },
        {
            "gender": 2,
            "age": 43,
            "value": "0.0008230000"
        },
        {
            "gender": 2,
            "age": 44,
            "value": "0.0008880000"
        },
        {
            "gender": 2,
            "age": 45,
            "value": "0.0010170000"
        },
        {
            "gender": 2,
            "age": 46,
            "value": "0.0010920000"
        },
        {
            "gender": 2,
            "age": 47,
            "value": "0.0011720000"
        },
        {
            "gender": 2,
            "age": 48,
            "value": "0.0012590000"
        },
        {
            "gender": 2,
            "age": 49,
            "value": "0.0013520000"
        },
        {
            "gender": 2,
            "age": 50,
            "value": "0.0014240000"
        },
        {
            "gender": 2,
            "age": 51,
            "value": "0.0015280000"
        },
        {
            "gender": 2,
            "age": 52,
            "value": "0.0016380000"
        },
        {
            "gender": 2,
            "age": 53,
            "value": "0.0017530000"
        },
        {
            "gender": 2,
            "age": 54,
            "value": "0.0018760000"
        },
        {
            "gender": 2,
            "age": 55,
            "value": "0.0021550000"
        },
        {
            "gender": 2,
            "age": 56,
            "value": "0.0023050000"
        },
        {
            "gender": 2,
            "age": 57,
            "value": "0.0024750000"
        },
        {
            "gender": 2,
            "age": 58,
            "value": "0.0026680000"
        },
        {
            "gender": 2,
            "age": 59,
            "value": "0.0028870000"
        },
        {
            "gender": 2,
            "age": 60,
            "value": "0.0033230000"
        },
        {
            "gender": 2,
            "age": 61,
            "value": "0.0036000000"
        },
        {
            "gender": 2,
            "age": 62,
            "value": "0.0039180000"
        },
        {
            "gender": 2,
            "age": 63,
            "value": "0.0042800000"
        },
        {
            "gender": 2,
            "age": 64,
            "value": "0.0046970000"
        },
        {
            "gender": 2,
            "age": 65,
            "value": "0.0055990000"
        },
        {
            "gender": 2,
            "age": 66,
            "value": "0.0061480000"
        },
        {
            "gender": 2,
            "age": 67,
            "value": "0.0067860000"
        },
        {
            "gender": 2,
            "age": 68,
            "value": "0.0075200000"
        },
        {
            "gender": 2,
            "age": 69,
            "value": "0.0083600000"
        },
        {
            "gender": 2,
            "age": 70,
            "value": "0.0097140000"
        },
        {
            "gender": 2,
            "age": 71,
            "value": "0.0108010000"
        },
        {
            "gender": 2,
            "age": 72,
            "value": "0.0120430000"
        },
        {
            "gender": 2,
            "age": 73,
            "value": "0.0134520000"
        },
        {
            "gender": 2,
            "age": 74,
            "value": "0.0150430000"
        },
        {
            "gender": 2,
            "age": 75,
            "value": "0.0163300000"
        },
        {
            "gender": 2,
            "age": 76,
            "value": "0.0183160000"
        },
        {
            "gender": 2,
            "age": 77,
            "value": "0.0205380000"
        },
        {
            "gender": 2,
            "age": 78,
            "value": "0.0230130000"
        },
        {
            "gender": 2,
            "age": 79,
            "value": "0.0257600000"
        },
        {
            "gender": 2,
            "age": 80,
            "value": "0.0287870000"
        },
        {
            "gender": 2,
            "age": 81,
            "value": "0.0321140000"
        },
        {
            "gender": 2,
            "age": 82,
            "value": "0.0357870000"
        },
        {
            "gender": 2,
            "age": 83,
            "value": "0.0398610000"
        },
        {
            "gender": 2,
            "age": 84,
            "value": "0.0444170000"
        },
        {
            "gender": 2,
            "age": 85,
            "value": "0.0495380000"
        },
        {
            "gender": 2,
            "age": 86,
            "value": "0.0553110000"
        },
        {
            "gender": 2,
            "age": 87,
            "value": "0.0618150000"
        },
        {
            "gender": 2,
            "age": 88,
            "value": "0.0691170000"
        },
        {
            "gender": 2,
            "age": 89,
            "value": "0.0772850000"
        },
        {
            "gender": 2,
            "age": 90,
            "value": "0.0863860000"
        },
        {
            "gender": 2,
            "age": 91,
            "value": "0.0964990000"
        },
        {
            "gender": 2,
            "age": 92,
            "value": "0.1077140000"
        },
        {
            "gender": 2,
            "age": 93,
            "value": "0.1201290000"
        },
        {
            "gender": 2,
            "age": 94,
            "value": "0.1338410000"
        },
        {
            "gender": 2,
            "age": 95,
            "value": "0.1489720000"
        },
        {
            "gender": 2,
            "age": 96,
            "value": "0.1656420000"
        },
        {
            "gender": 2,
            "age": 97,
            "value": "0.1839670000"
        },
        {
            "gender": 2,
            "age": 98,
            "value": "0.2040560000"
        },
        {
            "gender": 2,
            "age": 99,
            "value": "0.2260290000"
        },
        {
            "gender": 2,
            "age": 100,
            "value": "0.2499780000"
        },
        {
            "gender": 2,
            "age": 101,
            "value": "0.2759910000"
        },
        {
            "gender": 2,
            "age": 102,
            "value": "0.3041140000"
        },
        {
            "gender": 2,
            "age": 103,
            "value": "0.3343950000"
        },
        {
            "gender": 2,
            "age": 104,
            "value": "0.3668030000"
        },
        {
            "gender": 2,
            "age": 105,
            "value": "0.4012700000"
        },
        {
            "gender": 2,
            "age": 106,
            "value": "0.4488390000"
        },
        {
            "gender": 2,
            "age": 107,
            "value": "0.4987290000"
        },
        {
            "gender": 2,
            "age": 108,
            "value": "0.5565220000"
        },
        {
            "gender": 2,
            "age": 109,
            "value": "0.6194610000"
        },
        {
            "gender": 2,
            "age": 110,
            "value": "1.0000000000"
        }
    ]
}
response_data = create(data)
print('mortality-rate-create', response_data)

"""
刪除 mortality-rate 列表
mortality_rate_id 為 list_mortality_rates
"""
print('mortality-rate-delete', delete(response_data['data']['id']))
