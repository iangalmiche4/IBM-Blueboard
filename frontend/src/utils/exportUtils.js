/**
 * Export utilities for data tables
 * Supports CSV, Excel (XLSX), JSON, and PDF formats
 */

import { jsPDF } from "jspdf";
import autoTable from "jspdf-autotable";
import * as XLSX from "xlsx";

/**
 * Export data to CSV format
 * @param {Array} data - Array of objects to export
 * @param {Array} headers - Array of header objects with { key, header }
 * @param {string} filename - Name of the file (without extension)
 */
export const exportToCSV = (data, headers, filename = "export") => {
  if (!data || data.length === 0) {
    console.warn("No data to export");
    return;
  }

  // Create CSV header row
  const headerRow = headers.map((h) => h.header).join(",");

  // Create CSV data rows
  const dataRows = data.map((row) =>
    headers
      .map((h) => {
        const value = row[h.key];
        // Escape commas and quotes in values
        if (
          typeof value === "string" &&
          (value.includes(",") || value.includes('"'))
        ) {
          return `"${value.replace(/"/g, '""')}"`;
        }
        return value ?? "";
      })
      .join(","),
  );

  // Combine header and data
  const csv = [headerRow, ...dataRows].join("\n");

  // Create blob and download
  const blob = new Blob([csv], { type: "text/csv;charset=utf-8;" });
  downloadBlob(blob, `${filename}.csv`);
};

/**
 * Export data to Excel (XLSX) format
 * @param {Array} data - Array of objects to export
 * @param {Array} headers - Array of header objects with { key, header }
 * @param {string} filename - Name of the file (without extension)
 */
export const exportToExcel = (data, headers, filename = "export") => {
  if (!data || data.length === 0) {
    console.warn("No data to export");
    return;
  }

  // Create worksheet data with headers
  const wsData = [
    headers.map((h) => h.header),
    ...data.map((row) => headers.map((h) => row[h.key] ?? "")),
  ];

  // Create workbook and worksheet
  const wb = XLSX.utils.book_new();
  const ws = XLSX.utils.aoa_to_sheet(wsData);

  // Auto-size columns
  const colWidths = headers.map((h) => {
    const headerLength = h.header.length;
    const maxDataLength = Math.max(
      ...data.map((row) => String(row[h.key] ?? "").length),
    );
    return { wch: Math.max(headerLength, maxDataLength, 10) };
  });
  ws["!cols"] = colWidths;

  // Add worksheet to workbook
  XLSX.utils.book_append_sheet(wb, ws, "Data");

  // Write file
  XLSX.writeFile(wb, `${filename}.xlsx`);
};

/**
 * Export data to JSON format
 * @param {Array} data - Array of objects to export
 * @param {Array} headers - Array of header objects with { key, header }
 * @param {string} filename - Name of the file (without extension)
 */
export const exportToJSON = (data, headers, filename = "export") => {
  if (!data || data.length === 0) {
    console.warn("No data to export");
    return;
  }

  // Filter data to only include columns from headers
  const filteredData = data.map((row) => {
    const filtered = {};
    headers.forEach((h) => {
      filtered[h.key] = row[h.key];
    });
    return filtered;
  });

  // Create JSON string with pretty formatting
  const json = JSON.stringify(filteredData, null, 2);

  // Create blob and download
  const blob = new Blob([json], { type: "application/json;charset=utf-8;" });
  downloadBlob(blob, `${filename}.json`);
};

/**
 * Export data to PDF format
 * @param {Array} data - Array of objects to export
 * @param {Array} headers - Array of header objects with { key, header }
 * @param {string} filename - Name of the file (without extension)
 * @param {string} title - Title for the PDF document
 */
export const exportToPDF = (
  data,
  headers,
  filename = "export",
  title = "Data Export",
) => {
  if (!data || data.length === 0) {
    console.warn("No data to export");
    return;
  }

  // Create new PDF document
  const doc = new jsPDF();

  // Add title
  doc.setFontSize(16);
  doc.text(title, 14, 15);

  // Add timestamp
  doc.setFontSize(10);
  doc.text(`Generated: ${new Date().toLocaleString()}`, 14, 22);

  // Prepare table data
  const tableHeaders = headers.map((h) => h.header);
  const tableData = data.map((row) =>
    headers.map((h) => String(row[h.key] ?? "")),
  );

  // Add table using autoTable
  autoTable(doc, {
    head: [tableHeaders],
    body: tableData,
    startY: 28,
    styles: {
      fontSize: 8,
      cellPadding: 2,
    },
    headStyles: {
      fillColor: [22, 82, 240], // IBM Blue
      textColor: 255,
      fontStyle: "bold",
    },
    alternateRowStyles: {
      fillColor: [245, 245, 245],
    },
  });

  // Save PDF
  doc.save(`${filename}.pdf`);
};

/**
 * Export data based on format setting
 * @param {Array} data - Array of objects to export
 * @param {Array} headers - Array of header objects with { key, header }
 * @param {string} format - Export format (csv, xlsx, json, pdf)
 * @param {string} filename - Name of the file (without extension)
 * @param {string} title - Title for PDF (optional)
 */
export const exportData = (
  data,
  headers,
  format,
  filename = "export",
  title = "Data Export",
) => {
  switch (format.toLowerCase()) {
    case "csv":
      exportToCSV(data, headers, filename);
      break;
    case "xlsx":
      exportToExcel(data, headers, filename);
      break;
    case "json":
      exportToJSON(data, headers, filename);
      break;
    case "pdf":
      exportToPDF(data, headers, filename, title);
      break;
    default:
      console.error(`Unsupported export format: ${format}`);
  }
};

/**
 * Helper function to download a blob
 * @param {Blob} blob - Blob to download
 * @param {string} filename - Name of the file
 */
const downloadBlob = (blob, filename) => {
  const url = window.URL.createObjectURL(blob);
  const link = document.createElement("a");
  link.href = url;
  link.download = filename;
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  window.URL.revokeObjectURL(url);
};
