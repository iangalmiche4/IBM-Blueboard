import { useEffect, useState, useSyncExternalStore } from "react";
import { Download } from "@carbon/icons-react";
import {
  Button,
  DataTable,
  Pagination,
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableHeader,
  TableRow,
  TableToolbar,
  TableToolbarContent,
  TableToolbarSearch,
} from "@carbon/react";
import { useSettings } from "../../contexts/SettingsContext";
import { themeStore } from "../../store/ThemeStore";
import { exportData } from "../../utils/exportUtils";

/**
 * DataTableWrapper - Reusable wrapper for Carbon DataTable with search, sort, pagination, and export
 *
 * @param {Array} data - Raw data array
 * @param {Array} headers - Table headers with { key, header, isSortable } structure
 * @param {Function} rowMapper - Function to transform raw data into table rows
 * @param {string} searchPlaceholder - Placeholder text for search input (default: "Search...")
 * @param {Function} searchFilter - Custom search filter function (optional)
 * @param {Object} initialSort - Initial sort config { key, direction } (optional)
 * @param {Array} pageSizes - Available page sizes (default: [10, 20, 50])
 * @param {number} defaultPageSize - Default page size (default: 10)
 * @param {string} exportFilename - Base filename for exports (default: "data")
 * @param {string} exportTitle - Title for PDF exports (default: "Data Export")
 * @param {Function} exportMapper - Optional custom mapper for export (if not provided, uses rowMapper with text extraction)
 */
function DataTableWrapper({
  data = [],
  headers = [],
  rowMapper,
  searchPlaceholder = "Search...",
  searchFilter,
  initialSort = null,
  pageSizes = [10, 20, 50],
  defaultPageSize = 10,
  exportFilename = "data",
  exportTitle = "Data Export",
  exportMapper = null,
  tableId = null, // Optional unique ID for preserving pagination state
}) {
  const { settings } = useSettings();

  // Subscribe to theme changes to trigger re-render
  const theme = useSyncExternalStore(
    (callback) => themeStore.subscribe(callback),
    () => themeStore.getTheme(),
  );

  // Initialize state from saved table state if available
  const savedState = tableId ? themeStore.getTableState(tableId) : null;
  const [filteredData, setFilteredData] = useState(data);
  const [searchTerm, setSearchTerm] = useState("");
  const [currentPage, setCurrentPage] = useState(savedState?.currentPage || 1);
  const [pageSize, setPageSize] = useState(
    savedState?.pageSize || defaultPageSize,
  );
  const [sortInfo, setSortInfo] = useState(
    initialSort || { key: "", direction: "NONE" },
  );

  // Save table state whenever pagination changes
  useEffect(() => {
    if (tableId) {
      themeStore.saveTableState(tableId, { currentPage, pageSize });
    }
  }, [tableId, currentPage, pageSize]);

  // Restore pagination state when theme changes
  useEffect(() => {
    if (tableId) {
      const state = themeStore.getTableState(tableId);
      if (state) {
        setCurrentPage(state.currentPage);
        setPageSize(state.pageSize);
      }
    }
  }, [theme, tableId]);

  // Update filtered data when data or search term changes
  useEffect(() => {
    if (!searchTerm) {
      setFilteredData(data);
      return;
    }

    if (searchFilter) {
      // Use custom search filter if provided
      const filtered = data.filter((item) => searchFilter(item, searchTerm));
      setFilteredData(filtered);
    } else {
      // Default search: search in all string fields
      const filtered = data.filter((item) =>
        Object.values(item).some((value) =>
          String(value).toLowerCase().includes(searchTerm.toLowerCase()),
        ),
      );
      setFilteredData(filtered);
    }
    setCurrentPage(1);
  }, [data, searchTerm, searchFilter]);

  // Handle sorting
  const handleSort = (key, direction) => {
    setSortInfo({ key, direction });
    const sorted = [...filteredData].sort((a, b) => {
      let aVal = a[key];
      let bVal = b[key];

      // Handle numeric values
      if (typeof aVal === "number" && typeof bVal === "number") {
        return direction === "ASC" ? aVal - bVal : bVal - aVal;
      }

      // Handle date values
      if (aVal instanceof Date && bVal instanceof Date) {
        return direction === "ASC"
          ? aVal.getTime() - bVal.getTime()
          : bVal.getTime() - aVal.getTime();
      }

      // Handle string values
      if (typeof aVal === "string") {
        aVal = aVal.toLowerCase();
        bVal = String(bVal).toLowerCase();
      }

      if (direction === "ASC") {
        return aVal > bVal ? 1 : aVal < bVal ? -1 : 0;
      } else {
        return aVal < bVal ? 1 : aVal > bVal ? -1 : 0;
      }
    });
    setFilteredData(sorted);
  };

  // Handle export
  const handleExport = () => {
    if (filteredData.length === 0) {
      console.warn("No data to export");
      return;
    }

    let dataToExport;

    if (exportMapper) {
      // Use custom export mapper if provided
      dataToExport = filteredData.map(exportMapper);
    } else {
      // Map filtered data to get formatted values (as displayed in table)
      const mappedRows = filteredData.map(rowMapper);

      // Extract plain text values from mapped rows (remove React components)
      dataToExport = mappedRows.map((row) => {
        const plainRow = {};
        headers.forEach((header) => {
          const value = row[header.key];
          // If value is a React element, extract text content
          if (value && typeof value === "object" && value.props) {
            // For Tags and other components, get the text content
            plainRow[header.key] =
              value.props.children || value.props.title || String(value);
          } else {
            plainRow[header.key] = value;
          }
        });
        return plainRow;
      });
    }

    // Generate filename with timestamp
    const timestamp = new Date().toISOString().split("T")[0];
    const filename = `${exportFilename}_${timestamp}`;

    // Export using the format from settings
    exportData(
      dataToExport,
      headers,
      settings.exportFormat,
      filename,
      exportTitle,
    );
  };

  // Get paginated rows
  const getPaginatedRows = () => {
    const startIndex = (currentPage - 1) * pageSize;
    const endIndex = startIndex + pageSize;
    return filteredData.slice(startIndex, endIndex).map(rowMapper);
  };

  return (
    <DataTable rows={getPaginatedRows()} headers={headers} isSortable>
      {({
        rows,
        headers,
        getHeaderProps,
        getRowProps,
        getTableProps,
        getTableContainerProps,
      }) => (
        <TableContainer
          {...getTableContainerProps()}
          className="data-table-container"
        >
          <TableToolbar>
            <TableToolbarContent>
              <TableToolbarSearch
                placeholder={searchPlaceholder}
                onChange={(e) => setSearchTerm(e.target.value)}
              />
              <Button
                className="export-button"
                kind="ghost"
                renderIcon={Download}
                iconDescription="Export data"
                onClick={handleExport}
                disabled={filteredData.length === 0}
              >
                Export ({settings.exportFormat.toUpperCase()})
              </Button>
            </TableToolbarContent>
          </TableToolbar>
          <Table {...getTableProps()}>
            <TableHead>
              <TableRow>
                {headers.map((header) => (
                  <TableHeader
                    {...getHeaderProps({
                      header,
                      isSortable: header.isSortable,
                      onClick: () => {
                        if (header.isSortable) {
                          const newDirection =
                            sortInfo.key === header.key &&
                            sortInfo.direction === "ASC"
                              ? "DESC"
                              : "ASC";
                          handleSort(header.key, newDirection);
                        }
                      },
                    })}
                    key={header.key}
                    isSortable={header.isSortable}
                    sortDirection={
                      sortInfo.key === header.key ? sortInfo.direction : "NONE"
                    }
                  >
                    {header.header}
                  </TableHeader>
                ))}
              </TableRow>
            </TableHead>
            <TableBody>
              {rows.map((row) => (
                <TableRow {...getRowProps({ row })} key={row.id}>
                  {row.cells.map((cell) => (
                    <TableCell key={cell.id}>{cell.value}</TableCell>
                  ))}
                </TableRow>
              ))}
            </TableBody>
          </Table>
          <Pagination
            page={currentPage}
            pageSize={pageSize}
            pageSizes={pageSizes}
            totalItems={filteredData.length}
            onChange={({ page, pageSize }) => {
              setCurrentPage(page);
              setPageSize(pageSize);
            }}
          />
        </TableContainer>
      )}
    </DataTable>
  );
}

export default DataTableWrapper;
