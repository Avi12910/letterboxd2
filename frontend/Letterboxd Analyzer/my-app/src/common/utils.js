const getItemsCountAndRating = (data , item, minimum) => {
    const dataCopy = JSON.parse(JSON.stringify(data));
    const dataArray = Object.values(dataCopy)
    const count = dataArray.reduce((acc, movie) => {
        for (const i in movie['film_info'][item]) {
            const j = movie['film_info'][item][i]
            acc[j] = (acc[j] || 0) + 1;
        }
        return acc
    }, {})

    const ratings = dataArray.reduce((acc, movie) => {
        for (const i in movie['film_info'][item]) {
            if (movie['rating'] !== 'n/a') {
                const j = movie['film_info'][item][i]

                acc[j] = (acc[j] || { sum: 0, count: 0})
                acc[j]['sum'] += movie['rating'];
                acc[j]['count'] += 1
            }}
        return acc
    }, {})

    Object.keys(ratings).forEach((value) => {
        if (ratings[value]['count'] < minimum) {
            delete ratings[value]
        } else {
            ratings[value] = (ratings[value]['sum'] / ratings[value]['count']).toFixed(2)
        }
    });


    return [count, ratings];
}

export default getItemsCountAndRating;