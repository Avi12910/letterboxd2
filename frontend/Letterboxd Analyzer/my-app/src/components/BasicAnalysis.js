import { LineChart, Line, BarChart, Bar, XAxis, YAxis, CartesianGrid, Tooltip, Legend, ResponsiveContainer } from 'recharts';

const RatingsByYear = ({ data }) => {
    const dataArray = Object.values(data)

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
        if (movie['rating'] != 'n/a') {
            yearArray[i][1] += movie['rating']
            yearArray[i][2] += 1

        }
    });


    const transformedData = Object.keys(yearArray).map(date => ({
        year: date,
        count: yearArray[date][0],
        avg: yearArray[date][2] != 0 ? (yearArray[date][1] / yearArray[date][2]).toFixed(2) : 0
    }))

    console.log(transformedData)

    return (
        <div>
            <h3>Movies Watched per Year</h3>
            <ResponsiveContainer minWidth={100} minHeight={500}>
                <BarChart data ={transformedData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="year" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey = "count" fill="#8884d8"/>
                </BarChart>
            </ResponsiveContainer>
            <h3>Average Rating per Year</h3>
            <ResponsiveContainer minWidth={100} minHeight={500}>
                <BarChart data ={transformedData}>
                    <CartesianGrid strokeDasharray="3 3" />
                    <XAxis dataKey="year" />
                    <YAxis />
                    <Tooltip />
                    <Legend />
                    <Bar dataKey = "avg" fill="#8884d8"/>
                </BarChart>
            </ResponsiveContainer>
        </div>
    )

}

export default RatingsByYear;