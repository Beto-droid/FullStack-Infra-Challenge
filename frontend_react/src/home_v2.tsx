import React, { useState, useEffect } from 'react';
import Box from '@mui/material/Box';
import { DataGrid, GridColDef, GridPaginationModel } from '@mui/x-data-grid';
import { fetchOrders } from './api';
import { Container } from '@mui/material';

const columns: GridColDef[] = [
    { field: 'id', headerName: 'ID', width: 300 },
    { field: 'customer_name', headerName: 'Customer Name', width: 300 },
    { field: 'item', headerName: 'Item', width: 100 },
    { field: 'quantity', headerName: 'Quantity', type: 'number', width: 100 },
    { field: 'status', headerName: 'Status', width: 100 },
];

const Orders: React.FC = () => {
    const [orders, setOrders] = useState([]);
    const [totalOrders, setTotalOrders] = useState(0);
    const [page, setPage] = useState(0);
    const [pageSize, setPageSize] = useState(5);

    useEffect(() => {
        const loadOrders = async () => {
            const data = await fetchOrders(page + 1, pageSize);
            setOrders(data.results);
            setTotalOrders(data.count);
        };
        loadOrders();
    }, [page, pageSize]);

    const handlePaginationChange = (pagination: GridPaginationModel) => {
        setPage(pagination.page);
        setPageSize(pagination.pageSize);
    };

    return (
        <Container>
            <Box>
                <DataGrid
                    rows={orders}
                    columns={columns}
                    // pagination
                    paginationMode="server"
                    rowCount={totalOrders}
                    pageSizeOptions={[5, 10, 20]}
                    paginationModel={{ page, pageSize }}
                    onPaginationModelChange={handlePaginationChange}
                    loading={!orders.length}
                />
            </Box>
        </Container>
    );
};

export default Orders;

