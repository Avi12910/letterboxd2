import React, { useState } from 'react';
import { Table, Thead, Tbody, Tr, Th, Td, TableContainer } from '@chakra-ui/react';
import {
    Menu,
    MenuButton,
    MenuList,
    MenuItem,
    MenuItemOption,
    MenuGroup,
    MenuOptionGroup,
    MenuDivider,
    Button
  } from '@chakra-ui/react'

const DirectorAnalysis = ({ data }) => {
    const dataCopy = JSON.parse(JSON.stringify(data));
    const dataArray = Object.values(dataCopy)
    const [productionType, setProductionType] = useState('Director')

    const count = dataArray.reduce((acc, movie) => {
        for (const i in movie['film_info']['production']) {
            if (movie['film_info']['production'][i][1] === productionType) {
                const j = movie['film_info']['production'][i][0]
                acc[j] = (acc[j] || 0) + 1;
            }
        }
        return acc
    }, {})

    const ratings = dataArray.reduce((acc, movie) => {
        for (const i in movie['film_info']['production']) {
            if (movie['rating'] !== 'n/a') {
                if (movie['film_info']['production'][i][1] === productionType) {
                    const j = movie['film_info']['production'][i][0]

                    acc[j] = (acc[j] || { sum: 0, count: 0})
                    acc[j]['sum'] += movie['rating'];
                    acc[j]['count'] += 1
                }
            }}
        return acc
    }, {})

    Object.keys(ratings).forEach((value) => {
        if (ratings[value]['count'] < 3 || ratings[value]['count'] > 5) {
            delete ratings[value]
        } else {
            ratings[value] = (ratings[value]['sum'] / ratings[value]['count']).toFixed(2)
        }
    });

    const mostWatchedDirectors = Object.entries(count)
        .sort(([, countA], [, countB]) => countB - countA)
        .slice(0,5);
    
    const topDirectors = Object.entries(ratings)
        .sort(([, ratingA], [, ratingB]) => ratingB - ratingA)
        .slice(0,5);


    return (
        <div>
            <Menu>
            <MenuButton as={Button}>
                {productionType}
            </MenuButton>
            <MenuList>
                <MenuItem onClick={() => setProductionType('Director')}>Director</MenuItem>
                <MenuItem onClick={() => setProductionType('Composer')}>Composer</MenuItem>
                <MenuItem onClick={() => setProductionType('Writer')}>Writer</MenuItem>
            </MenuList>
            </Menu>
            <TableContainer>
                <Table variant="striped" colorScheme="teal">
                    <Thead>
                        <Tr>
                            <Th>Rank</Th>
                            <Th>Director</Th>
                            <Th>Count</Th>
                        </Tr>
                    </Thead>
                    <Tbody>
                        {mostWatchedDirectors.map(([director, count], index) => (
                            <Tr key={director}>
                                <Td>{index + 1}</Td>
                                <Td>{director}</Td>
                                <Td>{count}</Td>
                            </Tr>
                        ))}
                    </Tbody>
                </Table>
                <Table variant="striped" colorScheme="teal">
                    <Thead>
                        <Tr>
                            <Th>Rank</Th>
                            <Th>Actor</Th>
                            <Th>Average Rating</Th>
                        </Tr>
                    </Thead>
                    <Tbody>
                        {topDirectors.map(([director, count], index) => (
                            <Tr key={director}>
                                <Td>{index + 1}</Td>
                                <Td>{director}</Td>
                                <Td>{count}</Td>
                            </Tr>
                        ))}
                    </Tbody>
                </Table>
            </TableContainer>
        </div>
    );
}

export default DirectorAnalysis