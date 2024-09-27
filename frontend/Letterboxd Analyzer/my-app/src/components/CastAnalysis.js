import React from 'react';
import { Table, Thead, Tbody, Tr, Th, Td, TableContainer, Heading, HStack, TableCaption } from '@chakra-ui/react';
import getItemsCountAndRating from '../common/utils';

const CastAnalysis = ({ data }) => {
    const [actorCount, actorRating] = getItemsCountAndRating(data, 'cast', 4)
    
  
    const mostWatchedActors = Object.entries(actorCount)
        .sort(([, countA], [, countB]) => countB - countA)
        .slice(0,10);
        
    const topActors = Object.entries(actorRating)
        .sort(([, ratingA], [, ratingB]) => ratingB - ratingA)
        .slice(0,10);

    return (
        <div>
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
        </div>
    );
};

export default CastAnalysis;