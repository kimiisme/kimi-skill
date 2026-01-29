import json

with open(r'C:\Users\kimiisme\.claude\skills\workdays\scripts\cache\holiday_cache.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

year_data = data['2026']
holidays = [(k, v['note']) for k, v in year_data.items() if v['note'] not in ['普通工作日', '周末']]
makeup = [(k, v['note']) for k, v in year_data.items() if v['note'] == '补班工作日']
holidays.sort()
makeup.sort()

print('# 2026年 节假日')
for date, note in holidays:
    if note != '补班工作日':
        print(f'{date} - {note}')

print()
print('# 2026年 补班')
for date, note in makeup:
    print(f'{date} - {note}')
