document.addEventListener("DOMContentLoaded", () => {

    let parameter = document.getElementById('parameter').value || 1;
    let parameter2 = document.getElementById('pie').value || 1
    let parameter3 = document.getElementById('pie2').value || 1

    let url = `/inicio/grafico/vendas/${parameter}`;
    $.getJSON(url, function(data) {
        criarGrafico(data);
    });

    let url2 = `/inicio/grafico/categorias/${parameter2}`;
    $.getJSON(url2, function(data2) {
        criarGrafico2(data2);
    });

    let url3 = `/inicio/grafico/custos/${parameter3}`;
    $.getJSON(url3, function(data3) {
        criarGrafico3(data3);
    });
});

function criarGrafico(dados) {
    const series = Object.keys(dados).map(nomeSerie => {
        return {
            name: nomeSerie,
            data: dados[nomeSerie].map(ponto => [new Date(ponto.date).getTime(), ponto.value])
        };
    });

    new ApexCharts(document.querySelector('#reportsChart'), {
        series: series,
        chart: {
            height: 247,
            type: 'area',
            toolbar: {
                show: true
            }
        },
        markers: {
            size: 4
        },
        colors: ['#4154f1', '#2eca6a', '#dc143c'],
        fill: {
            type: 'gradient',
            gradient: {
                shadeIntensity: 1,
                opacityFrom: 0.3,
                opacityTo: 0.4,
                stops: [0, 90, 100]
            }
        },
        dataLabels: {
            enabled: false
        },
        stroke: {
            curve: 'smooth',
            width: 2
        },
        xaxis: {
            type: 'datetime'
        },
        tooltip: {
            x: {
                format: 'dd/MM/yy'
            }
        }
    }).render();
}

function criarGrafico2(dados) {

    echarts.init(document.querySelector("#trafficChart")).setOption({
        tooltip: {
            trigger: 'item',
            formatter: '{b}: <strong>{c} ({d}%)</strong>'
        },
        series: [{
            type: 'pie',
            radius: ['40%', '70%'],
            avoidLabelOverlap: false,
            label: {
                show: false,
                position: 'center'
            },
            emphasis: {
                label: {
                    show: true,
                    fontSize: '18',
                    fontWeight: 'bold'
                }
            },
            labelLine: {
                show: false
            },
            data: dados.map(function(item) {
                return {
                    name: item.name,
                    value: item.value.toLocaleString('pt-BR')
                };
            })
        }]
    });
}

function criarGrafico3(dados) {

    echarts.init(document.querySelector("#trafficChart2")).setOption({
        tooltip: {
            trigger: 'item',
            formatter: '{b}: <strong>R$ {c} ({d}%)</strong>'
        },
        series: [{
            type: 'pie',
            radius: ['40%', '70%'],
            avoidLabelOverlap: false,
            label: {
                show: false,
                position: 'center'
            },
            emphasis: {
                label: {
                    show: true,
                    fontSize: '18',
                    fontWeight: 'bold'
                }
            },
            labelLine: {
                show: false
            },
            data: dados.map(function(item) {
                return {
                    name: item.name,
                    value: item.value.toLocaleString('pt-BR')
                };
            })
        }]
    });    
}