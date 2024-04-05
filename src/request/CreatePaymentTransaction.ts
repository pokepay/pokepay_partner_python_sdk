// DO NOT EDIT: File is generated by code generator.

import { Request, Method } from "./Request";
import { TransactionDetail } from "../response/TransactionDetail";

class CreatePaymentTransaction implements Request<TransactionDetail> {
  public readonly __r: TransactionDetail | undefined;
  public readonly method: Method = "POST";
  public readonly path: string;
  public readonly bodyParams: {
    shop_id: string,
    customer_id: string,
    private_money_id: string,
    amount: number,
    description?: string,
    metadata?: string,
    products: Products,
    request_id?: string
  };
  public constructor(params: {
    shop_id: string,
    customer_id: string,
    private_money_id: string,
    amount: number,
    description?: string,
    metadata?: string,
    products: Products,
    request_id?: string
  }) {
    if (params.shop_id === void 0) throw new Error('"shop_id" is required');
    if (params.customer_id === void 0) throw new Error('"customer_id" is required');
    if (params.private_money_id === void 0) throw new Error('"private_money_id" is required');
    if (params.amount === void 0) throw new Error('"amount" is required');
    if (params.products === void 0) throw new Error('"products" is required');
    this.path = "/transactions" + "/payment";
    this.bodyParams = {
      shop_id: params.shop_id,
      customer_id: params.customer_id,
      private_money_id: params.private_money_id,
      amount: params.amount,
      products: params.products,
    };
    if (params.description !== void 0) this.bodyParams.description = params.description;
    if (params.metadata !== void 0) this.bodyParams.metadata = params.metadata;
    if (params.request_id !== void 0) this.bodyParams.request_id = params.request_id;
  }
}

export { CreatePaymentTransaction };
