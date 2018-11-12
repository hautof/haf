
var ID_TS_RECORDS = "ts-records";
var CLASS_TS_RECORD = "ts-record";
var CLASS_TC_RECORD = "tc-record";
var CLASS_TC_RECORD_RESULT = "tc-record-result";
var SELECTOR_CLASS_TS_RECORD = "." + CLASS_TS_RECORD;
var SELECTOR_CLASS_TC_RECORD = "." + CLASS_TC_RECORD;
var SELECTOR_CLASS_TC_RECORD_RESULT = "." + CLASS_TC_RECORD_RESULT;

function getComputedStylePropertyValue(element, property) {
    return window.getComputedStyle(element, null).getPropertyValue(property);
}


function stopEventPropagation(event) {
    event.stopPropagation();
}


function showTestCaseWithStatus(tcSelector, status, targetShouldChangeColor)
{
    showTestSuitesDetail();
    var elements = document.querySelectorAll(tcSelector);
    for(var i=0; i<elements.length; i++) {
        var element = elements[i];
        if(status == 'all') {
            element.style.display = 'table-row';
        }
        else {
            element.style.display = 'none';
        }
    }

    var elements = document.querySelectorAll(tcSelector + "."+status);
    for(var i=0; i<elements.length; i++) {
        var element = elements[i];
        element.style.display = 'table-row';
    }

    var ts_tables = document.querySelectorAll(SELECTOR_CLASS_TS_RECORD);
    var first_display_table = null;

    for(var j=0; j<ts_tables.length; j++) {
        var ts_table = ts_tables[j];
        ts_table.style.marginTop = null;
        var rows = ts_table.querySelectorAll(tcSelector)
        var hide = true;
        for(var i=0; i<rows.length; i++) {
            var row = rows[i];
            if(row.style.display != "none") {
                hide = false;
                break;
            }
        }
        if(hide)
            ts_table.style.display = "none";
        else {
            ts_table.style.display = "table";
            if(first_display_table == null)
                first_display_table = ts_table;
        }
    }

    if(first_display_table != null) {
        var margin_top = getComputedStylePropertyValue(ts_tables[0], "margin-top")
        first_display_table.style.marginTop = margin_top;
    }

    if (targetShouldChangeColor) {
        var elements = targetShouldChangeColor.parentElement.children;
        for(var i=0; i<elements.length; i++) {
            var element = elements[i];
            element.style.color = 'blue';
        }
        targetShouldChangeColor.style.color = 'purple';
    }
}


function toggleTestCaseResult(selector)
{
    var element = document.querySelector(selector);
    var current = element.currentStyle
                ? element.currentStyle['display']
                : getComputedStylePropertyValue(element, 'display');
    element.style.display = (current == 'none' ? "block" : 'none');

    parent = element.parentNode;

    while(parent && parent.tagName.toLowerCase() != "table") {
        parent = parent.parentNode;
    }
    var a = parent.querySelector(".operation>a");
    var elements = parent.querySelectorAll(SELECTOR_CLASS_TC_RECORD_RESULT);
    var text = "Collapse";
    for(var i=0; i < elements.length; i++) {
        if(getComputedStylePropertyValue(elements[i], 'display') == "none") {
            text = "Expand";
            break
        }
    }
    a.textContent = text;
}


function toggleTestSuiteResults(tsRecordId, toggleTarget){
    var tsRecord = document.getElementById(tsRecordId);
    tsRecord.style.display = "table";
    var a = tsRecord.querySelector(".operation>a");
    var toggleTarget = toggleTarget || a.textContent;
    var elements = tsRecord.querySelectorAll(SELECTOR_CLASS_TC_RECORD_RESULT);
    for(var i=0; i < elements.length; i++) {
        var element = elements[i];
        element.style.display = (toggleTarget == "Expand" ? "block" : "none");
    }

    if(toggleTarget == 'Expand')
        a.textContent = 'Collapse';
    else
        a.textContent = 'Expand';
}


function showTestSuitesDetail() {
    var tsRecordsElement = document.getElementById(ID_TS_RECORDS)
    tsRecordsElement.style.display = "block";
}


function onClickTestSuiteHref(tsRecordId) {
    showTestSuitesDetail();

    var element = document.getElementById("all-results-toggle")
    toggleAllResults(element, 'Collapse All')

    var tsElements = document.getElementsByClassName(CLASS_TS_RECORD)
    for(var i=0; i < tsElements.length; i++) {
        var element = tsElements[i];
        element.style.display = "none";
    }

    toggleTestSuiteResults(tsRecordId, "Collapse");
}


function toggleAllResults(target, toggleTarget) {
    // toggleTarget should be 'Expand All' or 'Collapse All'
    var toggleTarget = toggleTarget || target.textContent;
    var tsToggleTarget = toggleTarget == "Expand All" ? "Expand" : "Collapse";
    var tsRecords = document.getElementsByClassName(CLASS_TS_RECORD);
    for(var i=0; i < tsRecords.length; i++) {
        var tsRecord = tsRecords[i];
        toggleTestSuiteResults(tsRecord.id, tsToggleTarget);
    }
    target.textContent = toggleTarget == "Expand All" ? "Collapse All" : "Expand All";
}


function onCheckColumn(target, selector) {
    var checked = target.checked;
    var elements = document.querySelectorAll(selector);
    for(var i=0; i < elements.length; i++) {
        var element = elements[i];
        element.style.display = (checked ? "table-cell" : "none");
    }
}


function onDisplayResultParametersCheck(target, selector) {
    var showedName = "data-showed";
    var showedValue = target.getAttribute(showedName);
    var elements = document.querySelectorAll(selector);
    for(var i=0; i < elements.length; i++) {
        var element = elements[i];
        element.style.display = (!showedValue ? "block" : "none");
    }
    if (showedValue) {
        target.removeAttribute(showedName);
        target.style.color = "blue";
    } else {
        target.setAttribute(showedName, "true");
        target.style.color = "purple";
    }
}



function getStatistics(trElement){
    var td_notrun = trElement.querySelector("td.notrun");
    var td_passed = trElement.querySelector("td.passed");
    var td_warning = trElement.querySelector("td.warning");
    var td_skipped = trElement.querySelector("td.skipped");
    var td_failed = trElement.querySelector("td.failed");
    var td_erroneous = trElement.querySelector("td.erroneous");

    data = [
        {value: parseInt(td_notrun.textContent), name:'Not Run', itemStyle: { color: "#cdc0b0"}},
        {value: parseInt(td_passed.textContent), name:'Passed', itemStyle: { color: "#7ccd7c"}},
        {value: parseInt(td_warning.textContent), name:'Warning', itemStyle: { color: "#eeee00"}},
        {value: parseInt(td_skipped.textContent), name:'Skipped', itemStyle: { color: "#4f94cd"}},
        {value: parseInt(td_failed.textContent), name:'Failed', itemStyle: { color: "#cd5555"}},
        {value: parseInt(td_erroneous.textContent), name:'Erroneous', itemStyle: { color: "#9932cc"}},
    ];
    return data;
}


function getTimelineAndDurationDataGroupByStatus(tcRecordSelector) {
     var tcRecordElements = document.querySelectorAll(tcRecordSelector);
     var data = {
        notrun: [],
        passed: [],
        warning: [],
        failed: [],
        skipped: [],
        erroneous: []
     }
     for(var i=0; i < tcRecordElements.length; i++) {
        var tcRecordElement = tcRecordElements[i];
        var tcRecord = {
            id: tcRecordElement.getAttribute("id"),
            status: tcRecordElement.className.split(' ')[1].trim(),
            title: tcRecordElement.querySelector("td.column-title").textContent,
            path: tcRecordElement.querySelector("td.column-path").textContent,
            is_prerequisite: tcRecordElement.querySelector("td.column-is-prerequisite").textContent.toLowerCase() == "true" ? true : false,
            start_time: tcRecordElement.querySelector("td.column-start-time").textContent.trim(),
            finish_time: tcRecordElement.querySelector("td.column-finish-time").textContent.trim(),
            duration: parseFloat(tcRecordElement.querySelector("td.column-duration").textContent.trim().replace('s', '')),
        };

        middleTime = Date.parse(tcRecord.start_time) + (tcRecord.duration * 1000 / 2)
        data[tcRecord.status].push([middleTime, tcRecord.duration, tcRecord]);
     }
     return data;
}


function genSerieForStatus(status, data, color) {
    return {
        name: status,
        data: data,
        type: 'scatter',
        itemStyle: {
            color: color,
        }
    };
}


function jumpToRow(tcId) {
    var elements = document.getElementsByClassName(CLASS_TC_RECORD_RESULT);
    for(var i=0; i < elements.length; i++) {
        var element = elements[i];
        element.style.display = 'none';
    }
    var tcElement = document.querySelector('#' + tcId + ' ' + SELECTOR_CLASS_TC_RECORD_RESULT);
    tcElement.style.display = 'block';
}


function getTitle(tcRecordData, seriesName) {
    var call = "jumpToRow('" +  tcRecordData.id +"')";
    var a = '<a href="#' + tcRecordData.id + '" onclick="' + call + '">'
            + tcRecordData.title + ': ' + seriesName +
            '</a>';
    console.log(a);
    return a;
}


function updateChart(target, chartId, tsName, tsId) {
    var chartElement = document.getElementById(chartId);
    var chart = echarts.getInstanceByDom(chartElement);
    if (chart !== undefined) {
        var option = chart.getOption();
        var selector = SELECTOR_CLASS_TC_RECORD;
        if (tsId !== undefined) {
            selector = '#ts-' + tsId + " " + selector;
        }
        var data = getTimelineAndDurationDataGroupByStatus(selector);
        console.log(data);
        option.title[0].text = tsName;
        option.series[0].data = data.notrun;
        option.series[1].data = data.passed;
        option.series[2].data = data.warning;
        option.series[3].data = data.skipped;
        option.series[4].data = data.failed;
        option.series[5].data = data.erroneous;
        option.series[6].data = getStatistics(target);
        chart.setOption(option);
    }
}


function displayChart(chartDivElement, defaultDisplayTrId) {
    var chart = echarts.getInstanceByDom(chartDivElement);
    if (chart === undefined) {
        var data = getTimelineAndDurationDataGroupByStatus(SELECTOR_CLASS_TC_RECORD);
        chart = echarts.init(chartDivElement);
        var option = {
            title : {
                text: 'Total',
                x:'center'
            },
            tooltip: {enterable: true},
            grid: {
                width: '70%',
                left: '5%',
                containLabel: true,
                tooltip: {
                    borderColor: '#777',
                    borderWidth: 1,
                    formatter: function (obj) {
                        var record = obj.value[2];
                        return '<div style="border-bottom: 1px solid rgba(255,255,255,.3); font-size: 18px;padding-bottom: 7px;margin-bottom: 7px">'
                            + getTitle(record, obj.seriesName) + '</div>'
                            + 'Start Time: ' + record.start_time + '<br>'
                            + 'Finish Time: ' + record.finish_time + '<br>'
                            + 'Duration: ' + record.duration + 's<br>'
                            + 'Path: ' + record.path + '<br>'
                            + 'Is Prerequisite: ' + record.is_prerequisite + '<br>';
                    }
                },
            },
            xAxis: {
                type: 'time',
                name: 'Timeline',
                nameTextStyle: {
                    fontWeight: 'bold',
                },
                splitLine: {
                    show: true,
                    lineStyle: {
                        type: 'dashed'
                    }
                },
            },
            yAxis: {
                type: 'value',
                name: 'Duration(s)',
                nameTextStyle: {
                    fontWeight: 'bold',
                },
                splitLine: {
                    show: true,
                    lineStyle: {
                        type: 'dashed'
                    }
                },
            },
            legend: {
                x: 'center',
                y: 'bottom',
                data: [
                    { name: "Not Run", icon: 'rect' },
                    { name: "Passed", icon: 'rect' },
                    { name: "Warning", icon: 'rect' },
                    { name: "Skipped", icon: 'rect' },
                    { name: "Failed", icon: 'rect' },
                    { name: "Erroneous", icon: 'rect' },
                ],
            },

            series : [
                genSerieForStatus('Not Run', data.notrun, '#cdc0b0'),
                genSerieForStatus('Passed', data.passed, '#7ccd7c'),
                genSerieForStatus('Warning', data.warning, '#eeee00'),
                genSerieForStatus('Skipped', data.skipped, '#4f94cd'),
                genSerieForStatus('Failed', data.failed, '#cd5555'),
                genSerieForStatus('Erroneous', data.erroneous, '#9932cc'),

                {
                    name: 'TestCase',
                    type: 'pie',
                    radius : '60%',
                    center: ['88%', '50%'],
                    data: getStatistics(document.getElementById(defaultDisplayTrId)),
                    itemStyle: {
                        emphasis: {
                            shadowBlur: 10,
                            shadowOffsetX: 0,
                            shadowColor: 'rgba(0, 0, 0, 0.5)'
                        }
                    },
                    tooltip : {
                        trigger: 'item',
                        formatter: "{a} <br/>{b} : {c} ({d}%)"
                    },
                }
            ]
        };
        chart.setOption(option);
    }

}


function toggleChart(target, chartRowId, chartDivId, defaultDisplayTrId) {
    var chartRowElement = document.getElementById(chartRowId);
    var chartDivElement = document.getElementById(chartDivId);

    var a = target.querySelector('.operation>a')
    a.textContent = a.textContent === 'Show Chart' ? 'Hide Chart' : 'Show Chart';
    chartRowElement.style.display = chartRowElement.style.display === 'none' ? 'table-row' : 'none';

    displayChart(chartDivElement, defaultDisplayTrId)
}
