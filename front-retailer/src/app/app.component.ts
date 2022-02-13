import { Component, HostListener, OnInit } from '@angular/core';
import { GridOptions } from 'ag-grid-community';
import { Customer } from 'src/models/customer';
import { Invoice } from 'src/models/invoice';
import { InvoicePriceQuantityRatio } from 'src/models/invoicePriceQuantityRatio';
import { Product } from 'src/models/product';
import { ProductCountryDistribution } from 'src/models/productCountryDistribution';
import { ProductPriceDistribution } from 'src/models/productPriceDistribution';
import { TopProduct } from 'src/models/topProduct';
import { RetailerService } from 'src/services/retailer-service';

@Component({
  selector: 'app-root',
  templateUrl: './app.component.html',
  styleUrls: ['./app.component.scss']
})
export class AppComponent implements OnInit {

  title = 'front-retailer';

  public processingServer: number = 0;

  public topProduct: TopProduct;
  public bestCustomer: Customer;



  public productsAveragePrices: Array<Product>;

  public gridOptionsInvoice: GridOptions;
  public coldDefInvoice: Array<any>;
  public invoices: Array<Invoice>;

  public gridOptionsPriceRatio: GridOptions;
  public coldDefPriceRatio: Array<any>;
  public invoicesAveragePrices: Array<InvoicePriceQuantityRatio>;

  public gridOptionsCountryDistribution: GridOptions;
  public coldDefCountryDistribution: Array<any>;
  public productCountryDistributions: Array<ProductCountryDistribution>;

  public gridOptionsPriceDistribution: GridOptions;
  public coldDefPriceDistribution: Array<any>;
  public productPriceDistributions: Array<ProductPriceDistribution>;


  constructor(private readonly retailerService: RetailerService) {
    this.gridOptionsInvoice = this.createGridOptions();

    this.gridOptionsInvoice.getNodeChildDetails = this.getInvoiceProductChildren as any;

    this.gridOptionsPriceRatio = this.createGridOptions();
    this.gridOptionsCountryDistribution = this.createGridOptions();
    this.gridOptionsPriceDistribution = this.createGridOptions();

    this.coldDefInvoice = [
      {
        headerName: 'Id', field: 'id',
        cellRenderer: 'agGroupCellRenderer',
        cellRendererParams: {
          innerRenderer: this.innerGroupInvoiceRenderer
        }
      },
      { headerName: 'Date', field: 'date' },
      { headerName: 'Customer Id', field: 'customer.id' },
      { headerName: 'Country', field: 'country' },
      { headerName: 'Product stock code', field: 'stockCode' },
      { headerName: 'Product description', field: 'description' },
      { headerName: 'Product quantity', field: 'quantity' },
      { headerName: 'Product price', field: 'price' },
    ];

    this.coldDefPriceRatio = [
      { headerName: 'Invoice Id', field: 'invoiceId' },
      { headerName: 'Invoice Date', field: 'invoiceDate' },
      { headerName: 'Customer Id', field: 'customerId' },
      { headerName: 'Country', field: 'country' },
      { headerName: 'Price ratio', field: 'productPriceRatio' }
    ];

    this.coldDefCountryDistribution = [
      { headerName: 'Product stock code', field: 'stockCode' },
      { headerName: 'Product description', field: 'description' },
      { headerName: 'Country', field: 'country' },
      { headerName: 'Count', field: 'count' }
    ];

    this.coldDefPriceDistribution = [
      { headerName: 'Product stock code', field: 'stockCode' },
      { headerName: 'Product description', field: 'description' },
      { headerName: 'Average price', field: 'averagePrice' }
    ]
  }


  ngOnInit(): void {

    this.getInvoices();
    this.getTopProduct();
    this.getBestCustomer();
    this.getInvoicesAverageProductPrice();
    this.getProductDistributionByCountry();
    this.getProductAveragePrice();
  }

  private innerGroupInvoiceRenderer(param: any) {
    if (!param?.data?.id) {
      return '';
    }
    return param.data.id;
  }

  private getInvoiceProductChildren(rowItem: any) {
    if (rowItem?.products?.length > 0) {
      return {
        expanded: true,
        group: true,
        children: rowItem.products,
        key: rowItem.id
      }
    }
    return null;
  }

  private createGridOptions(): GridOptions {
    return {
      defaultColDef: {
        sortable: true,
        resizable: true,
        filter: true
      },
      headerHeight: 40
    } as GridOptions
  }

  public getInvoices(): void {
    this.processingServer++;
    this.retailerService.getInvoices().subscribe((invoices) => {
      this.processingServer--;
      this.invoices = invoices;
    }, (error) => {
      this.processingServer--;
      console.error(error)
    });
  }

  public getTopProduct(): void {
    this.processingServer++;
    this.retailerService.getTopProduct().subscribe((product) => {
      this.processingServer--;
      this.topProduct = product
    }, (error) => {
      this.processingServer--;
      console.error(error)
    });
  }

  public getBestCustomer(): void {
    this.processingServer++;
    this.retailerService.getBestCustomer().subscribe((customer) => {
      this.processingServer--;
      this.bestCustomer = customer;
    }, (error) => {
      this.processingServer--;
      console.error(error)
    });
  }

  public getInvoicesAverageProductPrice(): void {
    this.processingServer++;
    this.retailerService.getInvoicesAverageProductPrice().subscribe((invoicesAveragePrices) => {
      this.processingServer--;
      this.invoicesAveragePrices = invoicesAveragePrices;
    }, (error) => {
      this.processingServer--;
      console.error(error)
    })
  }

  public getProductDistributionByCountry(): void {
    this.processingServer++;
    this.retailerService.getProductDistributionByCountry().subscribe((productDistributionCountries) => {
      this.processingServer--;
      this.productCountryDistributions = productDistributionCountries;
    }, (error) => {
      this.processingServer--;
      console.error(error)
    })
  }

  public getProductAveragePrice(): void {
    this.processingServer++;
    this.retailerService.getProductAveragePrice().subscribe((productPriceDistributions) => {
      this.productPriceDistributions = productPriceDistributions;
      this.processingServer--;
    }, (error) => {
      this.processingServer--;
      console.error(error)
    });
  }

  @HostListener('window:reisze', ['$event'])
  public onResizeWindow() {
    this.resizeGrid(this.gridOptionsInvoice);
    this.resizeGrid(this.gridOptionsPriceRatio);
    this.resizeGrid(this.gridOptionsCountryDistribution);
    this.resizeGrid(this.gridOptionsPriceDistribution);
  }

  public resizeGrid(gridOption: GridOptions) {
    gridOption?.api?.sizeColumnsToFit();
  }

  public gridInvoiceReadyHandler() {
    this.resizeGrid(this.gridOptionsInvoice);
  }

  public gridPriceRatioReadyHandler() {
    this.resizeGrid(this.gridOptionsPriceRatio);
  }

  public gridCountryDistributionReadyHandler() {
    this.resizeGrid(this.gridOptionsCountryDistribution);
  }

  public gridPriceDistributionReadyHandler() {
    this.resizeGrid(this.gridOptionsPriceDistribution);
  }
}
