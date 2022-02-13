import { Injectable } from "@angular/core";
import { HttpClient } from "@angular/common/http";
import { Observable } from "rxjs";
import { Invoice } from "src/models/invoice";
import { Product } from "src/models/product";
import { Customer } from "src/models/customer";
import { InvoicePriceQuantityRatio } from "src/models/invoicePriceQuantityRatio";
import { ProductCountryDistribution } from "src/models/productCountryDistribution";
import { TopProduct } from "src/models/topProduct";
import { ProductPriceDistribution } from "src/models/productPriceDistribution";

@Injectable({
    providedIn: 'root'
})
export class RetailerService {

    private serviceUrl = "http://127.0.0.1:5000/api/v1"

    constructor(private readonly http: HttpClient) {

    }

    public getInvoices(): Observable<Array<Invoice>> {
        return this.http.get<Array<Invoice>>(`${this.serviceUrl}/invoice`);
    }

    public getTopProduct(): Observable<TopProduct> {
        return this.http.get<TopProduct>(`${this.serviceUrl}/product/top`);
    }

    public getBestCustomer(): Observable<Customer> {
        return this.http.get<Customer>(`${this.serviceUrl}/customer/top`);
    }

    public getInvoicesAverageProductPrice(): Observable<Array<InvoicePriceQuantityRatio>> {
        return this.http.get<Array<InvoicePriceQuantityRatio>>(`${this.serviceUrl}/invoice/price/quantity/ratio`);
    }

    public getProductDistributionByCountry(): Observable<Array<ProductCountryDistribution>> {
        return this.http.get<Array<ProductCountryDistribution>>(`${this.serviceUrl}/product/country`);
    }

    public getProductAveragePrice(): Observable<Array<ProductPriceDistribution>> {
        return this.http.get<Array<ProductPriceDistribution>>(`${this.serviceUrl}/product/average`);
    }
}