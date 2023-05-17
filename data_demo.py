data = [
 [
 [37, 189, ['', 'pratyushjava/Java_Algorithms_DataStructure', '', '', '', None, None, '', False, '', '', '', '', '', '', ''], 1, 70],
 [134, 263, ['https://joyfun.blog/2021/01/25/the-riemann-hypothesis-explained/', '', '', '', '', None, None, 'en', False, '', '', '', '', '', '', ''], 1, 2],
 [149, 313, ['http://en.wikipedia.org/wiki/Prime_number', '', '', None, '', None, None, '', False, '', '', '', '', '', '', ''], 1, 1]
 ]
]

links = []
for inner_list in data[0]:
    link = inner_list[2][0]
    if link:
        links.append(link)

print(links)
