import { Checkbox, Modal, ModalBody, ModalContent, useDisclosure } from "@chakra-ui/react";
import React, { useState } from "react"
import { BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const RatingsByYear = ({ data }) => {
    const dataArray = Object.values(data)
    const [selected, setSelected] = useState('')
    const { isOpen, onOpen, onClose } = useDisclosure()
    const [smoothOne, setSmoothOne] = useState(false)
    const [smoothTwo, setSmoothTwo] = useState(false)

    let minYear = 3000
    let maxYear = 0

    for (const i in dataArray) {
        const year = dataArray[i]['film_info']['year']

        if(year < minYear) {
            minYear = year
        }
        if (year > maxYear) {
            maxYear = year
        }
    }

    let yearArray = {}

    for (let i = minYear; i <= maxYear; i++) {
        yearArray[i] = [0,0,0]
    }

    dataArray.forEach(movie => {
        const i = movie['film_info']['year']
        yearArray[i][0] += 1
        if (movie['rating'] !== 'n/a') {
            yearArray[i][1] += movie['rating']
            yearArray[i][2] += 1

        }
    });


    const transformedData = Object.keys(yearArray).map(date => ({
        year: date,
        count: yearArray[date][0],
        avg: yearArray[date][2] !== 0 ? (yearArray[date][1] / yearArray[date][2]).toFixed(2) : 0
    }))

    let decadeArray = {}

    for (let i = Math.floor(minYear / 10); i <= Math.floor(maxYear / 10); i++) {
        decadeArray[i * 10] = [0,0,0]
    }

    dataArray.forEach(movie => {
        const i = Math.floor(movie['film_info']['year'] / 10) * 10
        decadeArray[i][0] += 1
        if (movie['rating'] !== 'n/a') {
            decadeArray[i][1] += movie['rating']
            decadeArray[i][2] += 1

        }
    });

    const transformedSmoothData = Object.keys(decadeArray).map(date => ({
        year: date,
        count: decadeArray[date][0],
        avg: decadeArray[date][2] !== 0 ? (decadeArray[date][1] / decadeArray[date][2]).toFixed(2) : 0
    }))

    const handleChartClick = (e) => {
        if (e && e.activePayload) {
            const year = e.activePayload[0].payload.year

            let movies = []

            if (smoothOne) {
                movies = dataArray.filter((movie) => {
                    return parseInt(year) === parseInt(movie['film_info']['year'])
                })
            }
            else {
                movies = dataArray.filter((movie) => {
                    return parseInt(movie['film_info']['year']) >= parseInt(year) &&
                        parseInt(movie['film_info']['year']) < parseInt(year) + 10
                })
            }

                movies = dataArray.filter((movie) => {
                return parseInt(year) === parseInt(movie['film_info']['year'])
            })

            if (movies.length > 0) {           
                setSelected(movies.map(movie => movie['film_info']['full_name'].slice(0,-7)))
                onOpen()
            }
        }
    }

    return (
        <div>
            <h3>Movies Watched per Year</h3>
            <Checkbox onChange={(e) => setSmoothOne(e.target.checked)}>Smooth</Checkbox>
            <ResponsiveContainer minWidth={100} minHeight={500}>
                <BarChart data ={smoothOne ? transformedSmoothData : transformedData} onClick={handleChartClick}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="year" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar 
                        dataKey = "count" fill="#8884d8"/>
                </BarChart>
            </ResponsiveContainer>
            <Modal isOpen={isOpen} onClose={onClose}>
                <ModalContent>
                    <ModalBody whiteSpace='pre-line'>
                        {selected.join('\n')}
                    </ModalBody>
                </ModalContent>
            </Modal>
            <h3>Average Rating per Year</h3>
            <Checkbox onChange={(e) => setSmoothTwo(e.target.checked)}>Smooth</Checkbox>
            <ResponsiveContainer minWidth={100} minHeight={500}>
                <BarChart data ={smoothTwo ? transformedSmoothData : transformedData} onClick={handleChartClick}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="year" />
                    <YAxis domain={[0,5]}/>
                    <Tooltip />
                    <Legend />
                    <Bar dataKey = "avg" fill="#8884d8"/>
                </BarChart>
            </ResponsiveContainer>
        </div>
    )

}

export default RatingsByYear;