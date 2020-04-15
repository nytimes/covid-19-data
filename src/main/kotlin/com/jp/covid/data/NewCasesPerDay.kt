package com.jp.covid.data

import javafx.application.Application
import javafx.collections.FXCollections
import javafx.collections.transformation.SortedList
import javafx.scene.Scene
import javafx.scene.chart.CategoryAxis
import javafx.scene.chart.LineChart
import javafx.scene.chart.NumberAxis
import javafx.scene.chart.XYChart
import javafx.scene.text.Font
import javafx.stage.Stage
import org.apache.commons.csv.CSVFormat
import org.apache.commons.csv.CSVRecord
import java.io.FileReader
import java.time.LocalDate
import java.time.format.DateTimeFormatter
import java.util.*
import java.util.stream.StreamSupport
import kotlin.collections.ArrayList
import kotlin.collections.HashMap

/**
 * Build using: ./gradlew build
 * Run using: ./gradlew run --args="new york"
 * OR
 * ./gradlew run --args "new york, washington, virginia"
 */
class NewCasesPerDay : Application() {

    companion object {
        private var states: Collection<String>? = null

        private val map: MutableMap<String, MutableCollection<StateRecord>> = HashMap()

        @JvmStatic
        fun main(args: Array<String>) {
            val input = args.joinToString(" ")
            states = input.split(",").map { s -> s.toLowerCase().trim() }
            (states as List<String>).stream().forEach { s -> println(s) }

            launch(NewCasesPerDay::class.java)
        }
    }

    override fun start(stage: Stage) {

        stage.title = "Covid-19 Chart"

        // Create chart
        val xAxis = CategoryAxis()
        val yAxis = NumberAxis()
        xAxis.label = "Date"
        xAxis.tickLabelFont = Font.font(15.0)
        yAxis.label = "Cases"
        val lineChart = LineChart(xAxis, yAxis)
        lineChart.axisSortingPolicy = LineChart.SortingPolicy.NONE

        // Get Data
        val fr = FileReader("us-states.csv")
        val records = CSVFormat.DEFAULT.withFirstRecordAsHeader().parse(fr)
        val spliterator = Spliterators.spliteratorUnknownSize(records.iterator(), Spliterator.ORDERED)
        val csvStream = StreamSupport.stream(spliterator, false)

        csvStream.filter { r -> states!!.contains(r.get("state").toLowerCase()) }
                .map { r -> getStateFromCsv(r) }
                .forEach { r -> addToMap(r) }

        map.entries.map { e -> getSeriesFromState(e.key, e.value) }
                .flatten()
                .forEach { s -> lineChart.data.add(s) }

        val scene = Scene(lineChart, 800.0, 600.0)

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
        result.date = LocalDate.parse(r.get("date"), DateTimeFormatter.ISO_DATE)
        result.totalCases = Integer.parseInt(r.get("cases"))
        result.state = r.get("state")

        return result
    }

    private fun getSeriesFromState(state: String, records: MutableCollection<StateRecord>): MutableCollection<XYChart.Series<String, Number>> {

        val result: MutableCollection<XYChart.Series<String, Number>> = ArrayList()

        val perDaySeries = XYChart.Series<String, Number>()
        perDaySeries.name = "$state New Cases"

        val totalCountSeries = XYChart.Series<String, Number>()
        totalCountSeries.name = "$state Total"

        val pdData = FXCollections.observableArrayList<XYChart.Data<String, Number>>()
        val tData = FXCollections.observableArrayList<XYChart.Data<String, Number>>()

        var floor = 0
        for (rec in records) {
            val perDay = rec.totalCases!! - floor
            floor = rec.totalCases!!
            val date = (rec.date!!.year * 10000) + (rec.date!!.month.value * 100) + rec.date!!.dayOfMonth

            if( rec.date!!.isBefore(LocalDate.of(2020,3,1))) {
                continue
            }

            pdData.add(XYChart.Data(date.toString(), perDay))
            tData.add(XYChart.Data(date.toString(), rec.totalCases!!))
        }

        val sortedTData = SortedList(tData, kotlin.Comparator { o1, o2 -> o1.xValue.compareTo(o2.xValue) })
        val sortedPdData = SortedList(pdData, kotlin.Comparator { o1, o2 -> o1.xValue.compareTo(o2.xValue) })


        totalCountSeries.data = sortedTData
        perDaySeries.data = sortedPdData

        result.add(perDaySeries)
        result.add(totalCountSeries)

        return result
    }
}