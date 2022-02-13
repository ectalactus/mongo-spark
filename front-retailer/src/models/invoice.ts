import { Customer } from "./customer";
import { Product } from "./product";

export class Invoice {
    id: number;
    date: Date;
    customer: Customer;
    country: string;
    products: Array<Product>;
}