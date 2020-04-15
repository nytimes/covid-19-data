package com.jp.covid.data

import javafx.application.Application
import javafx.scene.Scene
import javafx.scene.chart.CategoryAxis
import javafx.scene.chart.LineChart
import javafx.scene.chart.NumberAxis
import javafx.scene.chart.XYChart
import javafx.stage.Stage
import org.apache.commons.csv.CSVFormat
import org.apache.commons.csv.CSVRecord
import java.io.FileReader
import java.text.SimpleDateFormat
import java.time.LocalDate
import java.time.ZoneId
import java.util.*
import java.util.stream.Collectors
import java.util.stream.StreamSupport
import kotlin.collections.ArrayList
import kotlin.collections.HashMap

/**
 * Build using: ./gradlew build
 * Run using: ./gradlew run --args="new york"
 */
class NewCasesPerDay : Application() {

    companion object {
        private var state: String? = null
        private var states: MutableCollection<String>? = null
        val formatter = SimpleDateFormat("yyyy-MM-dd")

//        private val series: Map<String, MutableCollection<XYChart<String, Number>>> = HashMap()

        private val map: MutableMap<String, MutableCollection<StateRecord>> = HashMap()

        @JvmStatic
        fun main(args: Array<String>) {
            states = args.map { s -> s.toLowerCase() }.stream().collect(Collectors.toList())
            state = args.joinToString(separator = ",")
            launch(NewCasesPerDay::class.java)
        }
    }

    override fun start(stage: Stage) {

        stage.title = "Covid-19 Chart"

        // Create chart
        val xAxis = CategoryAxis()
        val yAxis = NumberAxis()
        xAxis.label = "Date"
        yAxis.label = "Cases"
        val lineChart = LineChart(xAxis, yAxis)
//        lineChart.title = "New Cases Per Day : $state"

        // Get Data
        val fr = FileReader("us-states.csv")
        val records = CSVFormat.DEFAULT.withFirstRecordAsHeader().parse(fr)
        val spliterator = Spliterators.spliteratorUnknownSize(records.iterator(), Spliterator.ORDERED)
        val csvStream = StreamSupport.stream(spliterator, false)

        csvStream.filter { r -> states!!.contains(r.get("state").toLowerCase()) }
                .map { r -> getStateFromCsv(r) }
                .forEach { r -> addToMap(r) }

        map.entries.map { e-> getSeriesFromState(e.key,e.value)}
                .flatMap { l -> l.stream() }



//        val stateRecords = csvStream
//                .filter { r -> r.get("state").equals(state, ignoreCase = true) }
//                .toArray()

        // Create Series
        val perDaySeries = XYChart.Series<String, Number>()
        perDaySeries.name = "New cases"

        val totalCountSeries = XYChart.Series<String, Number>()
        totalCountSeries.name = "total"


        var floor = 0
        for (rec in stateRecords) {
            val r = (rec as CSVRecord)
            val date = r.get("date").toString()
            val isOld = formatter.parse(date).toInstant().isBefore(LocalDate.now().minusDays(40).atStartOfDay(ZoneId.systemDefault()).toInstant())
            if (isOld) {
                continue
            }
            val cases: Int = Integer.parseInt((r.get("cases")))
            val perDay = cases - floor
            floor = cases
            perDaySeries.data.add(XYChart.Data(date, perDay))
            totalCountSeries.data.add(XYChart.Data(date, cases))
        }

        val scene = Scene(lineChart, 800.0, 600.0)
        lineChart.data.add(perDaySeries)
        lineChart.data.add(totalCountSeries)

        stage.scene = scene
        stage.show()
    }

    private fun addToMap(r: StateRecord) {

        if (!map.containsKey(r.state)) {
            map[r.state!!] = ArrayList()
        }

        map[r.state]!!.add(r)
    }

    private fun getStateFromCsv(r: CSVRecord): StateRecord {
        val result = StateRecord()
        result.date = r.get("date").toString()
        result.totalCases = Integer.parseInt(r.get("cases"))
        result.state = r.get("state")

        return result
    }

    private fun getSeriesFromState(state:String,records: MutableCollection<StateRecord>): MutableCollection<XYChart.Series<String,Number>> {

        val result: MutableCollection<XYChart.Series<String,Number>> = ArrayList()

        val perDaySeries = XYChart.Series<String, Number>()
        perDaySeries.name = "$state New Cases"

        val totalCountSeries = XYChart.Series<String, Number>()
        totalCountSeries.name = "$state Total"

        var floor = 0
        for (rec in records) {
            val perDay = rec.totalCases!! - floor
            floor = rec.totalCases!!
            perDaySeries.data.add(XYChart.Data(rec.date, perDay))
            totalCountSeries.data.add(XYChart.Data(rec.date, rec.totalCases))
        }

        result.add(perDaySeries)
        result.add(totalCountSeries)

        return result
    }
}