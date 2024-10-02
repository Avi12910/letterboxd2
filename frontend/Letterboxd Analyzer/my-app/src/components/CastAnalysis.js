import React, { useState } from 'react';
import { Box, Checkbox, Button, Table, Thead, Tbody, Tr, Th, Td, TableContainer, HStack, TableCaption } from '@chakra-ui/react';
import getItemsCountAndRating from '../common/utils';

const CastAnalysis = ({ data }) => {
    const [actorCount, actorRating] = getItemsCountAndRating(data, 'cast', 4)
    const [desc, setDesc] = useState(false)
    const [limit, setLimit] = useState(5)
    
  
    const mostWatchedActors = Object.entries(actorCount)
        .sort(([, countA], [, countB]) => desc ? countA - countB : countB - countA)
        .slice(0,limit);
        
    const topActors = Object.entries(actorRating)
        .sort(([, ratingA], [, ratingB]) => desc ? ratingA - ratingB : ratingB - ratingA)
        .slice(0,limit);

    return (
        <Box>
            <Checkbox onChange={(e) => setDesc(e.target.checked)}>Descending</Checkbox>
            <HStack spacing={8} align="start" w="100%">
                <TableContainer>
                    <Table variant="simple" colorScheme="teal">
                        <TableCaption placement = "top">
                            Most Watched Actors
                        </TableCaption>
                        <Thead>
                            <Tr>
                                <Th>Actor</Th>
                                <Th>Number of Movies</Th>
                            </Tr>
                        </Thead>
                        <Tbody>
                            {mostWatchedActors.map(([actor, count], index) => (
                                <Tr key={actor}>
                                    <Td>{actor}</Td>
                                    <Td>{count}</Td>
                                </Tr>
                            ))}
                        </Tbody>
                    </Table>
                </TableContainer>
                <TableContainer>
                    <Table variant="simple" colorScheme="teal">
                        <TableCaption placement="top">
                            Highest Rated Actors
                        </TableCaption>
                        <Thead>
                            <Tr>
                                <Th>Actor</Th>
                                <Th>Average Rating</Th>
                            </Tr>
                        </Thead>
                        <Tbody>
                            {topActors.map(([actor, count], index) => (
                                <Tr key={actor}>
                                    <Td>{actor}</Td>
                                    <Td>{count}</Td>
                                </Tr>
                            ))}
                        </Tbody>
                    </Table>
                </TableContainer>
            </HStack>
            <Button colorScheme='blue' onClick={() => setLimit(limit + 5)}>See More</Button>
        </Box>
    );
};

export default CastAnalysis;