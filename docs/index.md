# 自由现金流贴现法

For full documentation visit [mkdocs.org](https://www.mkdocs.org).

## 基本概念

DCF的英文全称是Discounted Cash Flow，当然如果是模型就加上Model，如果是估值就加上Valuation，翻译过来就是现金流贴现。

DCF方法的内涵就是把企业未来特定期间内的预期现金流还原为现值。很显然企业价值的真髓还是它未来盈利的能力，而盈利能力则体现为经营活动带来的现金流，因此理论界通常把现金流量贴现法作为企业价值的方法，在评估实践中也得到了大量的应用，并且已经日趋完善和成熟。

了解DCF估值法之前，我们必须要了解一个基本的概念，叫做贴现（或者叫折现），贴现的意思就是把未来的钱放到现在来衡量其价值，我们都知道由于通货膨胀的存在，现金购买力在下降，未来的100块的购买力肯定不如现在的100块，那么怎么定量计算呢。

我们举个栗子，假设现在猪肉价格是100块一斤，一年后105块，那么以猪肉为标的，1年后的105块折算到现在就是100块。以猪肉的价格为标准，我们可以得出一个贴现率=（105-100）/100=5%，即一年期的贴现率为5%，一年后的现金如果折算到现在都要除以（1+5%），如果这个值保持恒定，后一年的现金折算到现金需要除以2次（1+5%），以此类推。

## DCF的应用的要点及局限性
从基本的计算过程来看，DCF模型要比相对估值法更为复杂，主要原因是很多参数都要自己来设定，设定的过程中要考虑参数的合理性。我们先说一下几个参数，对于自由现金流D，为了方便计算我们可以直接选取净资产的收益，这个可以从年报中获得，贴现率r即为你持有该公司股份所期望的收益率，增长率则可以结合着公司自己的预测和市场对公司的看法来定一个值，有了这三个值就可以进行计算了，如果采用永续增长模型，一般采用与社会经济增长速度相当的值即可。


![QuickChart](https://quickchart.io/chart?c={type:'bar',data:{labels:['January','February','March','April','May'],datasets:{label:'Example Dataset',data:[65,59,80,81,56]}}})

![QuickChart](https://quickchart.io/chart?c=%7Btype:'bar',data:%7Blabels:%5B'January','February','March','April','May'%5D,datasets:%5B%7Blabel:'Example%20Dataset',data:%5B65,59,80,81,56%5D%7D%5D%7D)


![QuickChart](https://quickchart.io/chart?c={
"type": "bar",
"data": {
"labels": [
"January",
"February",
"March",
"April",
"May"
],
"datasets": [
{
"label": "Example Dataset",
"data": [
65,
59,
80,
81,
56
]
}
]
}
})


![柱状图111](https://quickchart.io/chart?c={type: 'bar',data: {labels:['a', 'B','C'],datasets:[{label:'Example',data:[5,10,15]}]}})


![柱状图111](https://quickchart.io/chart?c=%7B%22type%22%3A%20%22bar%22%2C%20%22data%22%3A%20%7B%22labels%22%3A%5B%22a%22%2C%20%22B%22%2C%22C%22%5D%2C%22datasets%22%3A%20%5B%7B%22label%22%3A%20%22Example%22%2C%22data%22%3A%20%5B5%2C10%2C15%5D%7D%5D%7D%7D)

![柱状图111](https://quickchart.io/chart?c={"type": "bar", "data": {"labels": ["a", "B", "C"], "datasets": [{"label": "Example", "data": [5, 10, 15]}]}})
