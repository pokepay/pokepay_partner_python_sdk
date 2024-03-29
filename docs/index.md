# Partner API SDK for NodeJS
## Installation

npmからインストールすることができます。
```
$ npm install --save pokepay-partner-sdk
```

プロジェクトにて、以下のようにロードできます。

```typescript
import ppsdk from "pokepay-partner-sdk";
// もしくは
import { Client, SendEcho } from "pokepay-partner-sdk";
```

## Getting started

基本的な使い方は次のようになります。

- ライブラリをロード
- 設定ファイル(後述)から `Client` オブジェクトを作る
- リクエストオブジェクトを作り、`Client` オブジェクトの `send` メソッドに対して渡す
- レスポンスオブジェクトを得る

```typescript
import { Client, SendEcho } from "pokepay-partner-sdk";
const client = new Client("/path/to/config.ini");
const request = new SendEcho({ message: 'hello' });
const response = await client.send(request);
```

レスポンスオブジェクト内にステータスコード、JSONをパースしたハッシュマップ、さらにレスポンス内容のオブジェクトが含まれています。

## Settings

設定はINIファイルに記述し、`Client` のコンストラクタにファイルパスを指定します。

SDKプロジェクトルートに `config.ini.sample` というファイルがありますのでそれを元に必要な情報を記述してください。特に以下の情報は通信の安全性のため必要な項目です。これらはパートナー契約時にお渡ししているものです。

- `CLIENT_ID`: パートナーAPI クライアントID
- `CLIENT_SECRET`: パートナーAPI クライアント秘密鍵
- `SSL_KEY_FILE`: SSL秘密鍵ファイルパス
- `SSL_CERT_FILE`: SSL証明書ファイルパス

この他に接続先のサーバURL情報が必要です。

- `API_BASE_URL`: パートナーAPI サーバURL

また、この設定ファイルには認証に必要な情報が含まれるため、ファイルの管理・取り扱いに十分注意してください。

設定ファイル記述例(`config.ini.sample`)

```
CLIENT_ID        = xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx
CLIENT_SECRET    = yyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyyy
API_BASE_URL     = https://partnerapi-sandbox.pokepay.jp
SSL_KEY_FILE     = /path/to/key.pem
SSL_CERT_FILE    = /path/to/cert.pem
```

## Overview

### APIリクエスト

Partner APIへの通信はリクエストオブジェクトを作り、`Client.send` メソッドに渡すことで行われます。
また `Client.send` は `async function` で `Promise` を返します。`await` することができます。
たとえば `SendEcho` は送信した内容をそのまま返す処理です。

```typescript
const request = new SendEcho({ message: 'hello' });
const response = await client.send(request);
# => Response 200 OK
```

通信の結果として、レスポンスオブジェクトが得られます。  
これはステータスコードとレスポンスボディ、各レスポンスクラスのオブジェクトをインスタンス変数に持つオブジェクトです。

```typescript
response.code
# => 200

response.body
# => {
  response_data: 'T7hZYdaXYRC0oC8oRrowte89690bYL3Ly05V-IiSzTCslQG-TH0e1i9QYNTySwVS9hiTD6u2---xojelG-66rA',
  timestamp: '2021-07-20T02:03:07.835Z',
  partner_call_id: '7cd52e4a-b9a2-48e4-b921-80dcbc6b7f4c'
}

response.object
# => { status: 'ok', message: 'hello' }

response.object.message
# => 'hello'
```

利用可能なAPI操作については [API Operations](#api-operations) で紹介します。

<a name="paging"></a>
### ページング

API操作によっては、大量のデータがある場合に備えてページング処理があります。
その処理では以下のようなプロパティを持つレスポンスオブジェクトを返します。

- rows : 列挙するレスポンスクラスのオブジェクトの配列
- count : 全体の要素数
- pagination : 以下のインスタンス変数を持つオブジェクト
  - current : 現在のページ位置(1からスタート)
  - per_page : 1ページ当たりの要素数
  - max_page : 最後のページ番号
  - has_prev : 前ページを持つかどうかの真理値
  - has_next : 次ページを持つかどうかの真理値

ページングクラスは `Pagination` で定義されています。

以下にコード例を示します。

```typescript
const request = new ListTransactions({ "page": 1, "per_page": 50 });
const response = await client.send(request);

if (response.object.pagination.has_next) {
  const next_page = response.object.pagination.current + 1;
  const request = new ListTransactions({ "page": next_page, "per_page": 50 });
  const response = await client.send(request);
}
```

### エラーハンドリング

JavaScript をご使用の場合、必須パラメーターがチェックされます。
TypeScript は型通りにお使いいただけます。

```javascript
const request = new SendEcho({});
=> Error: "message" is required;
```

API呼び出し時のエラーの場合は `axios` ライブラリのエラーが `throw` されます。
エラーレスポンスもステータスコードとレスポンスボディを持ちます。
参考: [axios handling errors](https://github.com/axios/axios#handling-errors)

```typescript
const axios = require('axios');

const request = SendEcho.new({ message: "hello" });

try {
  const response = await client.send(request);
} catch (error) {
  if (axios.isAxiosError(error)) {
    if (error.response) {
      // The request was made and the server responded with a status code
      // that falls out of the range of 2xx
      // APIサーバーがエラーレスポンス (2xx 以外) を返した場合
      console.log(error.response.data);
      console.log(error.response.status);
      console.log(error.response.headers);
    } else if (error.request) {
      // The request was made but no response was received
      // `error.request` is an instance of http.ClientRequest
      // リクエストは作られたが、レスポンスが受け取れなかった場合
      // `error.request` に `http.ClientRequest` が入ります
      console.log(error.request);
    } else {
      // Something happened in setting up the request that triggered an Error
      // リクエストを作る際に何かが起こった場合
      console.log('Error', error.message);
    }
  }
}
```
<a name="api-operations"></a>
## API Operations

- [GetCpmToken](#get-cpm-token): CPMトークンの状態取得
- [ListTransactions](#list-transactions): 【廃止】取引履歴を取得する
- [CreateTransaction](#create-transaction): 【廃止】チャージする
- [ListTransactionsV2](#list-transactions-v2): 取引履歴を取得する
- [CreateTopupTransaction](#create-topup-transaction): チャージする
- [CreatePaymentTransaction](#create-payment-transaction): 支払いする
- [CreateCpmTransaction](#create-cpm-transaction): CPMトークンによる取引作成
- [CreateTransferTransaction](#create-transfer-transaction): 個人間送金
- [CreateExchangeTransaction](#create-exchange-transaction): 
- [GetTransaction](#get-transaction): 取引情報を取得する
- [RefundTransaction](#refund-transaction): 取引をキャンセルする
- [GetTransactionByRequestId](#get-transaction-by-request-id): リクエストIDから取引情報を取得する
- [RequestUserStats](#request-user-stats): 指定期間内の顧客が行った取引の統計情報をCSVでダウンロードする
- [GetAccountTransferSummary](#get-account-transfer-summary): 
- [ListTransfers](#list-transfers): 
- [ListTransfersV2](#list-transfers-v2): 
- [CreateCheck](#create-check): チャージQRコードの発行
- [ListChecks](#list-checks): チャージQRコード一覧の取得
- [GetCheck](#get-check): チャージQRコードの表示
- [UpdateCheck](#update-check): チャージQRコードの更新
- [CreateTopupTransactionWithCheck](#create-topup-transaction-with-check): チャージQRコードを読み取ることでチャージする
- [ListBills](#list-bills): 支払いQRコード一覧を表示する
- [CreateBill](#create-bill): 支払いQRコードの発行
- [UpdateBill](#update-bill): 支払いQRコードの更新
- [CreateCashtray](#create-cashtray): Cashtrayを作る
- [GetCashtray](#get-cashtray): Cashtrayの情報を取得する
- [CancelCashtray](#cancel-cashtray): Cashtrayを無効化する
- [UpdateCashtray](#update-cashtray): Cashtrayの情報を更新する
- [GetAccount](#get-account): ウォレット情報を表示する
- [UpdateAccount](#update-account): ウォレット情報を更新する
- [DeleteAccount](#delete-account): ウォレットを退会する
- [ListAccountBalances](#list-account-balances): エンドユーザーの残高内訳を表示する
- [ListAccountExpiredBalances](#list-account-expired-balances): エンドユーザーの失効済みの残高内訳を表示する
- [UpdateCustomerAccount](#update-customer-account): エンドユーザーのウォレット情報を更新する
- [GetCustomerAccounts](#get-customer-accounts): エンドユーザーのウォレット一覧を表示する
- [CreateCustomerAccount](#create-customer-account): 新規エンドユーザーをウォレットと共に追加する
- [GetShopAccounts](#get-shop-accounts): 店舗ユーザーのウォレット一覧を表示する
- [ListCustomerTransactions](#list-customer-transactions): 取引履歴を取得する
- [ListOrganizations](#list-organizations): 加盟店組織の一覧を取得する
- [CreateOrganization](#create-organization): 新規加盟店組織を追加する
- [ListShops](#list-shops): 店舗一覧を取得する
- [CreateShop](#create-shop): 【廃止】新規店舗を追加する
- [CreateShopV2](#create-shop-v2): 新規店舗を追加する
- [GetShop](#get-shop): 店舗情報を表示する
- [UpdateShop](#update-shop): 店舗情報を更新する
- [ListUserAccounts](#list-user-accounts): エンドユーザー、店舗ユーザーのウォレット一覧を表示する
- [CreateUserAccount](#create-user-account): エンドユーザーのウォレットを作成する
- [GetPrivateMoneys](#get-private-moneys): マネー一覧を取得する
- [GetPrivateMoneyOrganizationSummaries](#get-private-money-organization-summaries): 決済加盟店の取引サマリを取得する
- [GetPrivateMoneySummary](#get-private-money-summary): 取引サマリを取得する
- [BulkCreateTransaction](#bulk-create-transaction): CSVファイル一括取引
- [CreateExternalTransaction](#create-external-transaction): ポケペイ外部取引を作成する
- [RefundExternalTransaction](#refund-external-transaction): ポケペイ外部取引をキャンセルする
- [CreateCampaign](#create-campaign): ポイント付与キャンペーンを作る
- [ListCampaigns](#list-campaigns): キャンペーン一覧を取得する
- [GetCampaign](#get-campaign): キャンペーンを取得する
- [UpdateCampaign](#update-campaign): ポイント付与キャンペーンを更新する
- [CreateWebhook](#create-webhook): webhookの作成
- [ListWebhooks](#list-webhooks): 作成したWebhookの一覧を返す
- [UpdateWebhook](#update-webhook): Webhookの更新
- [DeleteWebhook](#delete-webhook): Webhookの削除
- [ListCoupons](#list-coupons): クーポン一覧の取得
- [CreateCoupon](#create-coupon): クーポンの登録
- [GetCoupon](#get-coupon): クーポンの取得
- [UpdateCoupon](#update-coupon): クーポンの更新
- [CreateUserDevice](#create-user-device): ユーザーのデバイス登録
- [GetUserDevice](#get-user-device): ユーザーのデバイスを取得
- [ActivateUserDevice](#activate-user-device): デバイスの有効化
- [CreateBank](#create-bank): 銀行口座の登録
- [ListBanks](#list-banks): 登録した銀行の一覧
- [CreateBankTopupTransaction](#create-bank-topup-transaction): 銀行からのチャージ
### Transaction
<a name="get-cpm-token"></a>
#### CPMトークンの状態取得
CPMトークンの現在の状態を取得します。CPMトークンの有効期限やCPM取引の状態を返します。
```typescript
const response: Response<CpmToken> = await client.send(new GetCpmToken({
  cpm_token: "uGDOLqsy43AtWyT6hyzJkP" // CPMトークン
}));
```

---
`cpm_token`  
```json
{
  "type": "string",
  "minLength": 22,
  "maxLength": 22
}
```
CPM取引時にエンドユーザーが店舗に提示するバーコードを解析して得られる22桁の文字列です。

---
成功したときは[CpmToken](#cpm-token)オブジェクトを返します
<a name="list-transactions"></a>
#### 【廃止】取引履歴を取得する
取引一覧を返します。
```typescript
const response: Response<PaginatedTransaction> = await client.send(new ListTransactions({
  from: "2021-10-29T04:05:32.000000Z", // 開始日時
  to: "2021-09-14T01:13:45.000000Z", // 終了日時
  page: 1, // ページ番号
  per_page: 50, // 1ページ分の取引数
  shop_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // 店舗ID
  customer_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // エンドユーザーID
  customer_name: "太郎", // エンドユーザー名
  terminal_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // 端末ID
  transaction_id: "dv4Vr2ADh", // 取引ID
  organization_code: "pocketchange", // 組織コード
  private_money_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // マネーID
  is_modified: true, // キャンセルフラグ
  types: ["topup", "payment"], // 取引種別 (複数指定可)、チャージ=topup、支払い=payment
  description: "店頭QRコードによる支払い" // 取引説明文
}));
```

---
`from`  
```json
{
  "type": "string",
  "format": "date-time"
}
```
抽出期間の開始日時です。

フィルターとして使われ、開始日時以降に発生した取引のみ一覧に表示されます。

---
`to`  
```json
{
  "type": "string",
  "format": "date-time"
}
```
抽出期間の終了日時です。

フィルターとして使われ、終了日時以前に発生した取引のみ一覧に表示されます。

---
`page`  
```json
{
  "type": "integer",
  "minimum": 1
}
```
取得したいページ番号です。

---
`per_page`  
```json
{
  "type": "integer",
  "minimum": 1
}
```
1ページ分の取引数です。

---
`shop_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
店舗IDです。

フィルターとして使われ、指定された店舗での取引のみ一覧に表示されます。

---
`customer_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
エンドユーザーIDです。

フィルターとして使われ、指定されたエンドユーザーでの取引のみ一覧に表示されます。

---
`customer_name`  
```json
{
  "type": "string",
  "maxLength": 256
}
```
エンドユーザー名です。

フィルターとして使われ、入力された名前に部分一致するエンドユーザーでの取引のみ一覧に表示されます。

---
`terminal_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
端末IDです。

フィルターとして使われ、指定された端末での取引のみ一覧に表示されます。

---
`transaction_id`  
```json
{
  "type": "string"
}
```
取引IDです。

フィルターとして使われ、指定された取引IDに部分一致(前方一致)する取引のみが一覧に表示されます。

---
`organization_code`  
```json
{
  "type": "string",
  "maxLength": 32,
  "pattern": "^[a-zA-Z0-9-]*$"
}
```
組織コードです。

フィルターとして使われ、指定された組織での取引のみ一覧に表示されます。

---
`private_money_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
マネーIDです。

フィルターとして使われ、指定したマネーでの取引のみ一覧に表示されます。

---
`is_modified`  
```json
{
  "type": "boolean"
}
```
キャンセルフラグです。

これにtrueを指定するとキャンセルされた取引のみ一覧に表示されます。
デフォルト値はfalseで、キャンセルの有無にかかわらず一覧に表示されます。

---
`types`  
```json
{
  "type": "array",
  "items": {
    "type": "string",
    "enum": [
      "topup",
      "payment",
      "exchange_outflow",
      "exchange_inflow",
      "cashback",
      "expire"
    ]
  }
}
```
取引の種類でフィルターします。

以下の種類を指定できます。

1. topup
   店舗からエンドユーザーへの送金取引(チャージ)

2. payment
   エンドユーザーから店舗への送金取引(支払い)

3. exchange-outflow
   他マネーへの流出

4. exchange-inflow
   他マネーからの流入

5. cashback
   退会時返金取引

6. expire
   退会時失効取引

---
`description`  
```json
{
  "type": "string",
  "maxLength": 200
}
```
取引を指定の取引説明文でフィルターします。

取引説明文が完全一致する取引のみ抽出されます。取引説明文は最大200文字で記録されています。

---
成功したときは[PaginatedTransaction](#paginated-transaction)オブジェクトを返します
<a name="create-transaction"></a>
#### 【廃止】チャージする
チャージ取引を作成します。このAPIは廃止予定です。以降は `CreateTopupTransaction` を使用してください。
```typescript
const response: Response<TransactionDetail> = await client.send(new CreateTransaction({
  shop_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  customer_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  private_money_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  money_amount: 5908,
  point_amount: 238,
  point_expires_at: "2021-04-14T12:51:14.000000Z", // ポイント有効期限
  description: "2AhJrtrRhEmEhncAz9T8Jn6tKv842hmKtJWGe0W2JoBVxOBG6QSEaMM6DcJjfAtdrmKAg3KBKDu0vlbYdV"
}));
```

---
`point_expires_at`  
```json
{
  "type": "string",
  "format": "date-time"
}
```
ポイントをチャージした場合の、付与されるポイントの有効期限です。
省略した場合はマネーに設定された有効期限と同じものがポイントの有効期限となります。

---
成功したときは[TransactionDetail](#transaction-detail)オブジェクトを返します
<a name="list-transactions-v2"></a>
#### 取引履歴を取得する
取引一覧を返します。
```typescript
const response: Response<PaginatedTransactionV2> = await client.send(new ListTransactionsV2({
  private_money_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // マネーID
  organization_code: "pocketchange", // 組織コード
  shop_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // 店舗ID
  terminal_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // 端末ID
  customer_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // エンドユーザーID
  customer_name: "太郎", // エンドユーザー名
  description: "店頭QRコードによる支払い", // 取引説明文
  transaction_id: "6n9n", // 取引ID
  is_modified: true, // キャンセルフラグ
  types: ["topup", "payment"], // 取引種別 (複数指定可)、チャージ=topup、支払い=payment
  from: "2023-11-21T23:39:56.000000Z", // 開始日時
  to: "2020-11-05T05:28:40.000000Z", // 終了日時
  next_page_cursor_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // 次ページへ遷移する際に起点となるtransactionのID
  prev_page_cursor_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // 前ページへ遷移する際に起点となるtransactionのID
  per_page: 50 // 1ページ分の取引数
}));
```

---
`private_money_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
マネーIDです。

指定したマネーでの取引が一覧に表示されます。

---
`organization_code`  
```json
{
  "type": "string",
  "maxLength": 32,
  "pattern": "^[a-zA-Z0-9-]*$"
}
```
組織コードです。

フィルターとして使われ、指定された組織の店舗での取引のみ一覧に表示されます。

---
`shop_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
店舗IDです。

フィルターとして使われ、指定された店舗での取引のみ一覧に表示されます。

---
`terminal_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
端末IDです。

フィルターとして使われ、指定された端末での取引のみ一覧に表示されます。

---
`customer_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
エンドユーザーIDです。

フィルターとして使われ、指定されたエンドユーザーの取引のみ一覧に表示されます。

---
`customer_name`  
```json
{
  "type": "string",
  "maxLength": 256
}
```
エンドユーザー名です。

フィルターとして使われ、入力された名前に部分一致するエンドユーザーでの取引のみ一覧に表示されます。

---
`description`  
```json
{
  "type": "string",
  "maxLength": 200
}
```
取引を指定の取引説明文でフィルターします。

取引説明文が完全一致する取引のみ抽出されます。取引説明文は最大200文字で記録されています。

---
`transaction_id`  
```json
{
  "type": "string"
}
```
取引IDです。

フィルターとして使われ、指定された取引IDに部分一致(前方一致)する取引のみが一覧に表示されます。

---
`is_modified`  
```json
{
  "type": "boolean"
}
```
キャンセルフラグです。

これにtrueを指定するとキャンセルされた取引のみ一覧に表示されます。
デフォルト値はfalseで、キャンセルの有無にかかわらず一覧に表示されます。

---
`types`  
```json
{
  "type": "array",
  "items": {
    "type": "string",
    "enum": [
      "topup",
      "payment",
      "exchange_outflow",
      "exchange_inflow",
      "cashback",
      "expire"
    ]
  }
}
```
取引の種類でフィルターします。

以下の種類を指定できます。

1. topup
   店舗からエンドユーザーへの送金取引(チャージ)

2. payment
   エンドユーザーから店舗への送金取引(支払い)

3. exchange-outflow
   他マネーへの流出
   private_money_idが指定されたとき、そのマネーから見て流出方向の交換取引が抽出されます。
   private_money_idを省略した場合は表示されません。

4. exchange-inflow
   他マネーからの流入
   private_money_idが指定されたとき、そのマネーから見て流入方向の交換取引が抽出されます。
   private_money_idを省略した場合は表示されません。

5. cashback
   退会時返金取引

6. expire
   退会時失効取引

---
`from`  
```json
{
  "type": "string",
  "format": "date-time"
}
```
抽出期間の開始日時です。

フィルターとして使われ、開始日時以降に発生した取引のみ一覧に表示されます。

---
`to`  
```json
{
  "type": "string",
  "format": "date-time"
}
```
抽出期間の終了日時です。

フィルターとして使われ、終了日時以前に発生した取引のみ一覧に表示されます。

---
`next_page_cursor_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
次ページへ遷移する際に起点となるtransactionのID(前ページの末尾要素のID)です。
本APIのレスポンスにもnext_page_cursor_idが含まれており、これがnull値の場合は最後のページであることを意味します。
UUIDである場合は次のページが存在することを意味し、このnext_page_cursor_idをリクエストパラメータに含めることで次ページに遷移します。

next_page_cursor_idのtransaction自体は次のページには含まれません。

---
`prev_page_cursor_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
前ページへ遷移する際に起点となるtransactionのID(次ページの先頭要素のID)です。

本APIのレスポンスにもprev_page_cursor_idが含まれており、これがnull値の場合は先頭のページであることを意味します。
UUIDである場合は前のページが存在することを意味し、このprev_page_cursor_idをリクエストパラメータに含めることで前ページに遷移します。

prev_page_cursor_idのtransaction自体は前のページには含まれません。

---
`per_page`  
```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 1000
}
```
1ページ分の取引数です。

デフォルト値は50です。

---
成功したときは[PaginatedTransactionV2](#paginated-transaction-v2)オブジェクトを返します
<a name="create-topup-transaction"></a>
#### チャージする
チャージ取引を作成します。
```typescript
const response: Response<TransactionDetail> = await client.send(new CreateTopupTransaction({
  shop_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // 店舗ID
  customer_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // エンドユーザーのID
  private_money_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // マネーID
  bear_point_shop_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // ポイント支払時の負担店舗ID
  money_amount: 9868, // マネー額
  point_amount: 2287, // ポイント額
  point_expires_at: "2020-08-17T18:52:59.000000Z", // ポイント有効期限
  description: "初夏のチャージキャンペーン", // 取引履歴に表示する説明文
  metadata: "{\"key\":\"value\"}", // 取引メタデータ
  request_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" // リクエストID
}));
```

---
`shop_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
店舗IDです。

送金元の店舗を指定します。

---
`customer_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
エンドユーザーIDです。

送金先のエンドユーザーを指定します。

---
`private_money_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
マネーIDです。

マネーを指定します。

---
`bear_point_shop_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
ポイント支払時の負担店舗IDです。

ポイント支払い時に実際お金を負担する店舗を指定します。

---
`money_amount`  
```json
{
  "type": "integer",
  "minimum": 0
}
```
マネー額です。

送金するマネー額を指定します。
デフォルト値は0で、money_amountとpoint_amountの両方が0のときにはinvalid_parameter_both_point_and_money_are_zero(エラーコード400)が返ります。

---
`point_amount`  
```json
{
  "type": "integer",
  "minimum": 0
}
```
ポイント額です。

送金するポイント額を指定します。
デフォルト値は0で、money_amountとpoint_amountの両方が0のときにはinvalid_parameter_both_point_and_money_are_zero(エラーコード400)が返ります。

---
`point_expires_at`  
```json
{
  "type": "string",
  "format": "date-time"
}
```
ポイントをチャージした場合の、付与されるポイントの有効期限です。
省略した場合はマネーに設定された有効期限と同じものがポイントの有効期限となります。

---
`description`  
```json
{
  "type": "string",
  "maxLength": 200
}
```
取引説明文です。

任意入力で、取引履歴に表示される説明文です。

---
`metadata`  
```json
{
  "type": "string",
  "format": "json"
}
```
取引作成時に指定されるメタデータです。

任意入力で、全てのkeyとvalueが文字列であるようなフラットな構造のJSON文字列で指定します。

---
`request_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
取引作成APIの羃等性を担保するためのリクエスト固有のIDです。

取引作成APIで結果が受け取れなかったなどの理由で再試行する際に、二重に取引が作られてしまうことを防ぐために、クライアント側から指定されます。指定は任意で、UUID V4フォーマットでランダム生成した文字列です。リクエストIDは一定期間で削除されます。

リクエストIDを指定したとき、まだそのリクエストIDに対する取引がない場合、新規に取引が作られレスポンスとして返されます。もしそのリクエストIDに対する取引が既にある場合、既存の取引がレスポンスとして返されます。

---
成功したときは[TransactionDetail](#transaction-detail)オブジェクトを返します
<a name="create-payment-transaction"></a>
#### 支払いする
支払取引を作成します。
支払い時には、エンドユーザーの残高のうち、ポイント残高から優先的に消費されます。

```typescript
const response: Response<TransactionDetail> = await client.send(new CreatePaymentTransaction({
  shop_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // 店舗ID
  customer_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // エンドユーザーID
  private_money_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // マネーID
  amount: 7611, // 支払い額
  description: "たい焼き(小倉)", // 取引履歴に表示する説明文
  metadata: "{\"key\":\"value\"}", // 取引メタデータ
  products: [{"jan_code":"abc",
 "name":"name1",
 "unit_price":100,
 "price": 100,
 "is_discounted": false,
 "other":"{}"}, {"jan_code":"abc",
 "name":"name1",
 "unit_price":100,
 "price": 100,
 "is_discounted": false,
 "other":"{}"}], // 商品情報データ
  request_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" // リクエストID
}));
```

---
`shop_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
店舗IDです。

送金先の店舗を指定します。

---
`customer_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
エンドユーザーIDです。

送金元のエンドユーザーを指定します。

---
`private_money_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
マネーIDです。

マネーを指定します。

---
`amount`  
```json
{
  "type": "integer",
  "minimum": 0
}
```
マネー額です。

送金するマネー額を指定します。

---
`description`  
```json
{
  "type": "string",
  "maxLength": 200
}
```
取引説明文です。

任意入力で、取引履歴に表示される説明文です。

---
`metadata`  
```json
{
  "type": "string",
  "format": "json"
}
```
取引作成時に指定されるメタデータです。

任意入力で、全てのkeyとvalueが文字列であるようなフラットな構造のJSON文字列で指定します。

---
`products`  
```json
{
  "type": "array",
  "items": {
    "type": "object"
  }
}
```
一つの取引に含まれる商品情報データです。
以下の内容からなるJSONオブジェクトの配列で指定します。

- `jan_code`: JANコード。64字以下の文字列
- `name`: 商品名。256字以下の文字列
- `unit_price`: 商品単価。0以上の数値
- `price`: 全体の金額(例: 商品単価 × 個数)。0以上の数値
- `is_discounted`: 賞味期限が近いなどの理由で商品が値引きされているかどうかのフラグ。boolean
- `other`: その他商品に関する情報。JSONオブジェクトで指定します。

---
`request_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
取引作成APIの羃等性を担保するためのリクエスト固有のIDです。

取引作成APIで結果が受け取れなかったなどの理由で再試行する際に、二重に取引が作られてしまうことを防ぐために、クライアント側から指定されます。指定は任意で、UUID V4フォーマットでランダム生成した文字列です。リクエストIDは一定期間で削除されます。

リクエストIDを指定したとき、まだそのリクエストIDに対する取引がない場合、新規に取引が作られレスポンスとして返されます。もしそのリクエストIDに対する取引が既にある場合、既存の取引がレスポンスとして返されます。

---
成功したときは[TransactionDetail](#transaction-detail)オブジェクトを返します
<a name="create-cpm-transaction"></a>
#### CPMトークンによる取引作成
CPMトークンにより取引を作成します。
CPMトークンに設定されたスコープの取引を作ることができます。

```typescript
const response: Response<TransactionDetail> = await client.send(new CreateCpmTransaction({
  cpm_token: "3cE33CQPF6kxIlI0uguDnz", // CPMトークン
  shop_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // 店舗ID
  amount: 7017.0, // 取引金額
  description: "たい焼き(小倉)", // 取引説明文
  metadata: "{\"key\":\"value\"}", // 店舗側メタデータ
  products: [{"jan_code":"abc",
 "name":"name1",
 "unit_price":100,
 "price": 100,
 "is_discounted": false,
 "other":"{}"}, {"jan_code":"abc",
 "name":"name1",
 "unit_price":100,
 "price": 100,
 "is_discounted": false,
 "other":"{}"}, {"jan_code":"abc",
 "name":"name1",
 "unit_price":100,
 "price": 100,
 "is_discounted": false,
 "other":"{}"}], // 商品情報データ
  request_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" // リクエストID
}));
```

---
`cpm_token`  
```json
{
  "type": "string",
  "minLength": 22,
  "maxLength": 22
}
```
エンドユーザーによって作られ、アプリなどに表示され、店舗に対して提示される22桁の文字列です。

エンドユーザーによって許可された取引のスコープを持っています。

---
`shop_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
店舗IDです。

支払いやチャージを行う店舗を指定します。

---
`amount`  
```json
{
  "type": "number"
}
```
取引金額を指定します。

正の値を与えるとチャージになり、負の値を与えると支払いとなります。

---
`description`  
```json
{
  "type": "string",
  "maxLength": 200
}
```
取引説明文です。

エンドユーザーアプリの取引履歴などに表示されます。

---
`metadata`  
```json
{
  "type": "string",
  "format": "json"
}
```
取引作成時に店舗側から指定されるメタデータです。

任意入力で、全てのkeyとvalueが文字列であるようなフラットな構造のJSON文字列で指定します。

---
`products`  
```json
{
  "type": "array",
  "items": {
    "type": "object"
  }
}
```
一つの取引に含まれる商品情報データです。
以下の内容からなるJSONオブジェクトの配列で指定します。

- `jan_code`: JANコード。64字以下の文字列
- `name`: 商品名。256字以下の文字列
- `unit_price`: 商品単価。0以上の数値
- `price`: 全体の金額(例: 商品単価 × 個数)。0以上の数値
- `is_discounted`: 賞味期限が近いなどの理由で商品が値引きされているかどうかのフラグ。boolean
- `other`: その他商品に関する情報。JSONオブジェクトで指定します。

---
`request_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
取引作成APIの羃等性を担保するためのリクエスト固有のIDです。

取引作成APIで結果が受け取れなかったなどの理由で再試行する際に、二重に取引が作られてしまうことを防ぐために、クライアント側から指定されます。指定は任意で、UUID V4フォーマットでランダム生成した文字列です。リクエストIDは一定期間で削除されます。

リクエストIDを指定したとき、まだそのリクエストIDに対する取引がない場合、新規に取引が作られレスポンスとして返されます。もしそのリクエストIDに対する取引が既にある場合、既存の取引がレスポンスとして返されます。

---
成功したときは[TransactionDetail](#transaction-detail)オブジェクトを返します
<a name="create-transfer-transaction"></a>
#### 個人間送金
エンドユーザー間での送金取引(個人間送金)を作成します。
個人間送金で送れるのはマネーのみで、ポイントを送ることはできません。送金元のマネー残高のうち、有効期限が最も遠いものから順に送金されます。

```typescript
const response: Response<TransactionDetail> = await client.send(new CreateTransferTransaction({
  sender_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // 送金元ユーザーID
  receiver_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // 受取ユーザーID
  private_money_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // マネーID
  amount: 4244.0, // 送金額
  metadata: "{\"key\":\"value\"}", // 取引メタデータ
  description: "たい焼き(小倉)", // 取引履歴に表示する説明文
  request_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" // リクエストID
}));
```

---
`sender_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
エンドユーザーIDです。

送金元のエンドユーザー(送り主)を指定します。

---
`receiver_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
エンドユーザーIDです。

送金先のエンドユーザー(受け取り人)を指定します。

---
`private_money_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
マネーIDです。

マネーを指定します。

---
`amount`  
```json
{
  "type": "number",
  "minimum": 0
}
```
マネー額です。

送金するマネー額を指定します。

---
`metadata`  
```json
{
  "type": "string",
  "format": "json"
}
```
取引作成時に指定されるメタデータです。

任意入力で、全てのkeyとvalueが文字列であるようなフラットな構造のJSON文字列で指定します。

---
`description`  
```json
{
  "type": "string",
  "maxLength": 200
}
```
取引説明文です。

任意入力で、取引履歴に表示される説明文です。

---
`request_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
取引作成APIの羃等性を担保するためのリクエスト固有のIDです。

取引作成APIで結果が受け取れなかったなどの理由で再試行する際に、二重に取引が作られてしまうことを防ぐために、クライアント側から指定されます。指定は任意で、UUID V4フォーマットでランダム生成した文字列です。リクエストIDは一定期間で削除されます。

リクエストIDを指定したとき、まだそのリクエストIDに対する取引がない場合、新規に取引が作られレスポンスとして返されます。もしそのリクエストIDに対する取引が既にある場合、既存の取引がレスポンスとして返されます。

---
成功したときは[TransactionDetail](#transaction-detail)オブジェクトを返します
<a name="create-exchange-transaction"></a>
#### 
```typescript
const response: Response<TransactionDetail> = await client.send(new CreateExchangeTransaction({
  user_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  sender_private_money_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  receiver_private_money_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  amount: 4322,
  description: "NYM7VX5YLnlD8HOOCDlP4GZ7jbmXMO5zVMwfk3fyCehTHNb57OPgysrQCIrNbKg5EGtS1CRG8HTOfVnvp3qGXZFBsOSpPHbliv7UIdhUMzObVJcG5btiH5rur7GsubMGTjIcOXKD9o8Kba3",
  request_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" // リクエストID
}));
```

---
`request_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
取引作成APIの羃等性を担保するためのリクエスト固有のIDです。

取引作成APIで結果が受け取れなかったなどの理由で再試行する際に、二重に取引が作られてしまうことを防ぐために、クライアント側から指定されます。指定は任意で、UUID V4フォーマットでランダム生成した文字列です。リクエストIDは一定期間で削除されます。

リクエストIDを指定したとき、まだそのリクエストIDに対する取引がない場合、新規に取引が作られレスポンスとして返されます。もしそのリクエストIDに対する取引が既にある場合、既存の取引がレスポンスとして返されます。

---
成功したときは[TransactionDetail](#transaction-detail)オブジェクトを返します
<a name="get-transaction"></a>
#### 取引情報を取得する
取引を取得します。
```typescript
const response: Response<TransactionDetail> = await client.send(new GetTransaction({
  transaction_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" // 取引ID
}));
```

---
`transaction_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
取引IDです。

フィルターとして使われ、指定した取引IDの取引を取得します。

---
成功したときは[TransactionDetail](#transaction-detail)オブジェクトを返します
<a name="refund-transaction"></a>
#### 取引をキャンセルする
取引IDを指定して取引をキャンセルします。

発行体の管理者は自組織の直営店、または発行しているマネーの決済加盟店組織での取引をキャンセルできます。
キャンセル対象の取引に付随するポイント還元キャンペーンやクーポン適用も取り消されます。

チャージ取引のキャンセル時に返金すべき残高が足りないときは `account_balance_not_enough (422)` エラーが返ります。
取引をキャンセルできるのは1回きりです。既にキャンセルされた取引を重ねてキャンセルしようとすると `transaction_already_refunded (422)` エラーが返ります。
```typescript
const response: Response<TransactionDetail> = await client.send(new RefundTransaction({
  transaction_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // 取引ID
  description: "返品対応のため", // 取引履歴に表示する返金事由
  returning_point_expires_at: "2021-07-25T19:14:10.000000Z" // 返却ポイントの有効期限
}));
```

---
`returning_point_expires_at`  
```json
{
  "type": "string",
  "format": "date-time"
}
```
ポイント支払いを含む支払い取引をキャンセルする際にユーザへ返却されるポイントの有効期限です。デフォルトでは未指定です。

---
成功したときは[TransactionDetail](#transaction-detail)オブジェクトを返します
<a name="get-transaction-by-request-id"></a>
#### リクエストIDから取引情報を取得する
取引を取得します。
```typescript
const response: Response<TransactionDetail> = await client.send(new GetTransactionByRequestId({
  request_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" // リクエストID
}));
```

---
`request_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
取引作成時にクライアントが生成し指定するリクエストIDです。

リクエストIDに対応する取引が存在すればその取引を返し、無ければNotFound(404)を返します。

---
成功したときは[TransactionDetail](#transaction-detail)オブジェクトを返します
<a name="request-user-stats"></a>
#### 指定期間内の顧客が行った取引の統計情報をCSVでダウンロードする
期間を指定して、期間内に発行マネーの全顧客が行った取引の総額・回数などをCSVでダウンロードする機能です。
CSVの作成は非同期で行われるため完了まで少しの間待つ必要がありますが、完了時にダウンロードできるURLをレスポンスとして返します。
このURLの有効期限はリクエスト日時から7日間です。

ダウンロードできるCSVのデータは以下のものです。

* organization_code: 取引を行った組織コード
* private_money_id: 取引されたマネーのID
* private_money_name: 取引されたマネーの名前
* user_id: 決済したユーザーID
* user_external_id: 決済したユーザーの外部ID
* payment_money_amount: 指定期間内に決済に使ったマネーの総額
* payment_point_amount: 指定期間内に決済に使ったポイントの総額
* payment_transaction_count: 指定期間内に決済した回数。キャンセルされた取引は含まない

また、指定期間より前の決済を時間をおいてキャンセルした場合などには payment_money_amount, payment_point_amount, payment_transaction_count が負の値になることもあることに留意してください。
```typescript
const response: Response<UserStatsOperation> = await client.send(new RequestUserStats({
  from: "2022-05-20T17:56:49.000000+09:00", // 集計期間の開始時刻
  to: "2023-12-10T01:16:11.000000+09:00" // 集計期間の終了時刻
}));
```

---
`from`  
```json
{
  "type": "string",
  "format": "date-time"
}
```
集計する期間の開始時刻をISO8601形式で指定します。
時刻は現在時刻、及び `to` で指定する時刻以前である必要があります。

---
`to`  
```json
{
  "type": "string",
  "format": "date-time"
}
```
集計する期間の終了時刻をISO8601形式で指定します。
時刻は現在時刻、及び `from` で指定する時刻の間である必要があります。

---
成功したときは[UserStatsOperation](#user-stats-operation)オブジェクトを返します
### Transfer
<a name="get-account-transfer-summary"></a>
#### 
ウォレットを指定して取引明細種別毎の集計を返す
```typescript
const response: Response<AccountTransferSummary> = await client.send(new GetAccountTransferSummary({
  account_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // ウォレットID
  from: "2023-10-08T11:07:38.000000Z", // 集計期間の開始時刻
  to: "2022-03-06T17:42:32.000000Z", // 集計期間の終了時刻
  transfer_types: ["topup", "payment"] // 取引明細種別 (複数指定可)
}));
```

---
`account_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
ウォレットIDです。

ここで指定したウォレットIDの取引明細レベルでの集計を取得します。

---
`transfer_types`  
```json
{
  "type": "array",
  "items": {
    "type": "string",
    "enum": [
      "payment",
      "topup",
      "campaign-topup",
      "use-coupon",
      "refund-payment",
      "refund-topup",
      "refund-campaign",
      "refund-coupon",
      "exchange-inflow",
      "exchange-outflow",
      "refund-exchange-inflow",
      "refund-exchange-outflow"
    ]
  }
}
```
取引明細の種別でフィルターします。
以下の種別を指定できます。

- payment
  エンドユーザーから店舗への送金取引(支払い取引)
- topup
  店舗からエンドユーザーへの送金取引(チャージ取引)
- campaign-topup
  キャンペーンによるエンドユーザーへのポイント付与取引(ポイントチャージ)
- use-coupon
  支払い時のクーポン使用による値引き取引
- refund-payment
  支払い取引に対するキャンセル取引
- refund-topup
  チャージ取引に対するキャンセル取引
- refund-campaign
  キャンペーンによるポイント付与取引に対するキャンセル取引
- refund-coupon
  クーポン使用による値引き取引に対するキャンセル取引
- exchange-inflow
  交換による他マネーからの流入取引
- exchange-outflow
  交換による他マネーへの流出取引
- refund-exchange-inflow
  交換による他マネーからの流入取引に対するキャンセル取引
- refund-exchange-outflow
  交換による他マネーへの流出取引に対するキャンセル取引

---
成功したときは[AccountTransferSummary](#account-transfer-summary)オブジェクトを返します
<a name="list-transfers"></a>
#### 
```typescript
const response: Response<PaginatedTransfers> = await client.send(new ListTransfers({
  from: "2020-11-23T13:17:35.000000Z",
  to: "2022-06-30T21:15:53.000000Z",
  page: 6600,
  per_page: 7718,
  shop_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  shop_name: "BURahT5P9DvE8UV0j2YqC15yVJZpc8KVpH",
  customer_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  customer_name: "ARBDgg1",
  transaction_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  private_money_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  is_modified: true,
  transaction_types: ["expire"],
  transfer_types: ["cashback", "coupon", "topup", "transfer", "exchange", "campaign", "payment", "expire"], // 取引明細の種類でフィルターします。
  description: "店頭QRコードによる支払い" // 取引詳細説明文
}));
```

---
`transfer_types`  
```json
{
  "type": "array",
  "items": {
    "type": "string",
    "enum": [
      "topup",
      "payment",
      "exchange",
      "transfer",
      "coupon",
      "campaign",
      "cashback",
      "expire"
    ]
  }
}
```
取引明細の種類でフィルターします。

以下の種類を指定できます。

1. topup
店舗からエンドユーザーへの送金取引(チャージ)、またはそのキャンセル取引

2. payment
エンドユーザーから店舗への送金取引(支払い)、またはそのキャンセル取引

3. exchange
他マネーへの流出/流入

4. campaign
取引に対するポイント還元キャンペーンによるポイント付与、またはそのキャンセル取引

5. coupon
クーポンによる値引き処理、またはそのキャンセル取引

6. cashback
退会時の返金取引

7. expire
退会時失効取引

---
`description`  
```json
{
  "type": "string",
  "maxLength": 200
}
```
取引詳細を指定の取引詳細説明文でフィルターします。

取引詳細説明文が完全一致する取引のみ抽出されます。取引詳細説明文は最大200文字で記録されています。

---
成功したときは[PaginatedTransfers](#paginated-transfers)オブジェクトを返します
<a name="list-transfers-v2"></a>
#### 
```typescript
const response: Response<PaginatedTransfersV2> = await client.send(new ListTransfersV2({
  shop_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // 店舗ID
  shop_name: "cmC1vS6JUWIFuWHifSCeHqDX4OovF1kPsfFAfUD6hedBMnO5c5siBhPS0PdEUgltcrxJuLRpPyEyLzg5USUF0acnAYj9bCB7rUqwv3jfmweeo8gmjkrVbM4yoFbYRleOf9KOkq0RFzjJHwRArvOU8komJ1Atk5R", // 店舗名
  customer_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // エンドユーザーID
  customer_name: "lui7mGRMrDuzhgMwi2QEwxvEfxvbfoaYN92mmS964bSnGq9n7PpIOomMWW66P3IlH0kXmsTMdugDsmRtGnF7L4k", // エンドユーザー名
  transaction_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // 取引ID
  private_money_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // マネーID
  is_modified: false, // キャンセルフラグ
  transaction_types: ["cashback", "topup"], // 取引種別 (複数指定可)、チャージ=topup、支払い=payment
  next_page_cursor_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // 次ページへ遷移する際に起点となるtransferのID
  prev_page_cursor_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // 前ページへ遷移する際に起点となるtransferのID
  per_page: 50, // 1ページ分の取引数
  transfer_types: ["expire", "transfer"], // 取引明細種別 (複数指定可)
  description: "店頭QRコードによる支払い", // 取引詳細説明文
  from: "2023-02-15T14:34:28.000000Z", // 開始日時
  to: "2023-04-18T00:39:59.000000Z" // 終了日時
}));
```

---
`shop_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
店舗IDです。

フィルターとして使われ、指定された店舗での取引のみ一覧に表示されます。

---
`shop_name`  
```json
{
  "type": "string",
  "maxLength": 256
}
```
店舗名です。

フィルターとして使われ、入力された名前に部分一致する店舗での取引のみ一覧に表示されます。

---
`customer_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
エンドユーザーIDです。

フィルターとして使われ、指定されたエンドユーザーの取引のみ一覧に表示されます。

---
`customer_name`  
```json
{
  "type": "string",
  "maxLength": 256
}
```
エンドユーザー名です。

フィルターとして使われ、入力された名前に部分一致するエンドユーザーでの取引のみ一覧に表示されます。

---
`transaction_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
取引IDです。

フィルターとして使われ、指定された取引IDに部分一致(前方一致)する取引のみが一覧に表示されます。

---
`private_money_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
マネーIDです。

指定したマネーでの取引が一覧に表示されます。

---
`is_modified`  
```json
{
  "type": "boolean"
}
```
キャンセルフラグです。

これにtrueを指定するとキャンセルされた取引のみ一覧に表示されます。
デフォルト値はfalseで、キャンセルの有無にかかわらず一覧に表示されます。

---
`transaction_types`  
```json
{
  "type": "array",
  "items": {
    "type": "string",
    "enum": [
      "topup",
      "payment",
      "transfer",
      "exchange",
      "cashback",
      "expire"
    ]
  }
}
```
取引の種類でフィルターします。

以下の種類を指定できます。

1. topup
   店舗からエンドユーザーへの送金取引(チャージ)

2. payment
   エンドユーザーから店舗への送金取引(支払い)

3. exchange-outflow
   他マネーへの流出
   private_money_idが指定されたとき、そのマネーから見て流出方向の交換取引が抽出されます。
   private_money_idを省略した場合は表示されません。

4. exchange-inflow
   他マネーからの流入
   private_money_idが指定されたとき、そのマネーから見て流入方向の交換取引が抽出されます。
   private_money_idを省略した場合は表示されません。

5. cashback
   退会時返金取引

6. expire
   退会時失効取引

---
`next_page_cursor_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
次ページへ遷移する際に起点となるtransferのID(前ページの末尾要素のID)です。
本APIのレスポンスにもnext_page_cursor_idが含まれており、これがnull値の場合は最後のページであることを意味します。
UUIDである場合は次のページが存在することを意味し、このnext_page_cursor_idをリクエストパラメータに含めることで次ページに遷移します。

next_page_cursor_idのtransfer自体は次のページには含まれません。

---
`prev_page_cursor_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
前ページへ遷移する際に起点となるtransferのID(次ページの先頭要素のID)です。

本APIのレスポンスにもprev_page_cursor_idが含まれており、これがnull値の場合は先頭のページであることを意味します。
UUIDである場合は前のページが存在することを意味し、このprev_page_cursor_idをリクエストパラメータに含めることで前ページに遷移します。

prev_page_cursor_idのtransfer自体は前のページには含まれません。

---
`per_page`  
```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 1000
}
```
1ページ分の取引数です。

デフォルト値は50です。

---
`transfer_types`  
```json
{
  "type": "array",
  "items": {
    "type": "string",
    "enum": [
      "topup",
      "payment",
      "exchange",
      "transfer",
      "coupon",
      "campaign",
      "cashback",
      "expire"
    ]
  }
}
```
取引明細の種類でフィルターします。

以下の種類を指定できます。

1. topup
店舗からエンドユーザーへの送金取引(チャージ)、またはそのキャンセル取引

2. payment
エンドユーザーから店舗への送金取引(支払い)、またはそのキャンセル取引

3. exchange
他マネーへの流出/流入

4. campaign
取引に対するポイント還元キャンペーンによるポイント付与、またはそのキャンセル取引

5. coupon
クーポンによる値引き処理、またはそのキャンセル取引

6. cashback
退会時の返金取引

7. expire
退会時失効取引

---
`description`  
```json
{
  "type": "string",
  "maxLength": 200
}
```
取引詳細を指定の取引詳細説明文でフィルターします。

取引詳細説明文が完全一致する取引のみ抽出されます。取引詳細説明文は最大200文字で記録されています。

---
`from`  
```json
{
  "type": "string",
  "format": "date-time"
}
```
抽出期間の開始日時です。

フィルターとして使われ、開始日時以降に発生した取引のみ一覧に表示されます。

---
`to`  
```json
{
  "type": "string",
  "format": "date-time"
}
```
抽出期間の終了日時です。

フィルターとして使われ、終了日時以前に発生した取引のみ一覧に表示されます。

---
成功したときは[PaginatedTransfersV2](#paginated-transfers-v2)オブジェクトを返します
### Check
店舗ユーザが発行し、エンドユーザーがポケペイアプリから読み取ることでチャージ取引が発生するQRコードです。

チャージQRコードを解析すると次のようなURLになります(URLは環境によって異なります)。

`https://www-sandbox.pokepay.jp/checks/xxxxxxxx-xxxx-xxxxxxxxx-xxxxxxxxxxxx`

QRコードを読み取る方法以外にも、このURLリンクを直接スマートフォン(iOS/Android)上で開くことによりアプリが起動して取引が行われます。(注意: 上記URLはsandbox環境であるため、アプリもsandbox環境のものである必要があります) 上記URL中の `xxxxxxxx-xxxx-xxxxxxxxx-xxxxxxxxxxxx` の部分がチャージQRコードのIDです。

<a name="create-check"></a>
#### チャージQRコードの発行
```typescript
const response: Response<Check> = await client.send(new CreateCheck({
  account_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // 送金元の店舗アカウントID
  money_amount: 935.0, // 付与マネー額
  point_amount: 2607.0, // 付与ポイント額
  description: "test check", // 説明文(アプリ上で取引の説明文として表示される)
  is_onetime: false, // ワンタイムかどうかのフラグ
  usage_limit: 4146, // ワンタイムでない場合の最大読み取り回数
  expires_at: "2021-08-06T05:57:27.000000Z", // チャージQRコード自体の失効日時
  point_expires_at: "2023-09-18T07:29:12.000000Z", // チャージQRコードによって付与されるポイント残高の有効期限
  point_expires_in_days: 60, // チャージQRコードによって付与されるポイント残高の有効期限(相対日数指定)
  bear_point_account: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" // ポイント額を負担する店舗のウォレットID
}));
```
`money_amount`と`point_amount`の少なくとも一方は指定する必要があります。


---
`money_amount`  
```json
{
  "type": "number",
  "format": "decimal",
  "minimum": 0
}
```
チャージQRコードによって付与されるマネー額です。
`money_amount`と`point_amount`の少なくともどちらかは指定する必要があります。


---
`point_amount`  
```json
{
  "type": "number",
  "format": "decimal",
  "minimum": 0
}
```
チャージQRコードによって付与されるポイント額です。
`money_amount`と`point_amount`の少なくともどちらかは指定する必要があります。


---
`is_onetime`  
```json
{
  "type": "boolean"
}
```
チャージQRコードが一度の読み取りで失効するときに`true`にします。デフォルト値は`true`です。
`false`の場合、複数ユーザによって読み取り可能なQRコードになります。
ただし、その場合も1ユーザにつき1回のみしか読み取れません。


---
`usage_limit`  
```json
{
  "type": "integer"
}
```
複数ユーザによって読み取り可能なチャージQRコードの最大読み取り回数を指定します。
NULLに設定すると無制限に読み取り可能なチャージQRコードになります。
デフォルト値はNULLです。
ワンタイム指定(`is_onetime`)がされているときは、本パラメータはNULLである必要があります。


---
`expires_at`  
```json
{
  "type": "string",
  "format": "date-time"
}
```
チャージQRコード自体の失効日時を指定します。この日時以降はチャージQRコードを読み取れなくなります。デフォルトでは作成日時から3ヶ月後になります。

チャージQRコード自体の失効日時であって、チャージQRコードによって付与されるマネー残高の有効期限とは異なることに注意してください。マネー残高の有効期限はマネー設定で指定されているものになります。


---
`point_expires_at`  
```json
{
  "type": "string",
  "format": "date-time"
}
```
チャージQRコードによって付与されるポイント残高の有効起源を指定します。デフォルトではマネー残高の有効期限と同じものが指定されます。

チャージQRコードにより付与されるマネー残高の有効期限はQRコード毎には指定できませんが、ポイント残高の有効期限は本パラメータにより、QRコード毎に個別に指定することができます。


---
`point_expires_in_days`  
```json
{
  "type": "integer",
  "minimum": 1
}
```
チャージQRコードによって付与されるポイント残高の有効期限を相対日数で指定します。
1を指定すると、チャージQRコード作成日の当日中に失効します(翌日0時に失効)。
`point_expires_at`と`point_expires_in_days`が両方指定されている場合は、チャージQRコードによるチャージ取引ができた時点からより近い方が採用されます。


---
`bear_point_account`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
ポイントチャージをする場合、ポイント額を負担する店舗のウォレットIDを指定することができます。
デフォルトではマネー発行体のデフォルト店舗(本店)がポイント負担先となります。


---
成功したときは[Check](#check)オブジェクトを返します
<a name="list-checks"></a>
#### チャージQRコード一覧の取得
```typescript
const response: Response<PaginatedChecks> = await client.send(new ListChecks({
  page: 7969, // ページ番号
  per_page: 50, // 1ページの表示数
  private_money_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // マネーID
  organization_code: "cI", // 組織コード
  expires_from: "2021-06-12T19:58:59.000000Z", // 有効期限の期間によるフィルター(開始時点)
  expires_to: "2022-12-03T23:21:29.000000Z", // 有効期限の期間によるフィルター(終了時点)
  created_from: "2020-06-25T13:13:54.000000Z", // 作成日時の期間によるフィルター(開始時点)
  created_to: "2022-07-01T05:15:53.000000Z", // 作成日時の期間によるフィルター(終了時点)
  issuer_shop_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // 発行店舗ID
  description: "ayD2", // チャージQRコードの説明文
  is_onetime: false, // ワンタイムのチャージQRコードかどうか
  is_disabled: false // 無効化されたチャージQRコードかどうか
}));
```

---
`per_page`  
```json
{
  "type": "integer",
  "minimum": 1
}
```
1ページ当たり表示数です。デフォルト値は50です。

---
`private_money_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
チャージQRコードのチャージ対象のマネーIDで結果をフィルターします。


---
`organization_code`  
```json
{
  "type": "string",
  "maxLength": 32
}
```
チャージQRコードの発行店舗の所属組織の組織コードで結果をフィルターします。
デフォルトでは未指定です。

---
`expires_from`  
```json
{
  "type": "string",
  "format": "date-time"
}
```
有効期限の期間によるフィルターの開始時点のタイムスタンプです。
デフォルトでは未指定です。


---
`expires_to`  
```json
{
  "type": "string",
  "format": "date-time"
}
```
有効期限の期間によるフィルターの終了時点のタイムスタンプです。
デフォルトでは未指定です。


---
`created_from`  
```json
{
  "type": "string",
  "format": "date-time"
}
```
作成日時の期間によるフィルターの開始時点のタイムスタンプです。
デフォルトでは未指定です。


---
`created_to`  
```json
{
  "type": "string",
  "format": "date-time"
}
```
作成日時の期間によるフィルターの終了時点のタイムスタンプです。
デフォルトでは未指定です。


---
`issuer_shop_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
チャージQRコードを発行した店舗IDによってフィルターします。
デフォルトでは未指定です。


---
`description`  
```json
{
  "type": "string"
}
```
チャージQRコードの説明文(description)によってフィルターします。
部分一致(前方一致)したものを表示します。
デフォルトでは未指定です。


---
`is_onetime`  
```json
{
  "type": "boolean"
}
```
チャージQRコードがワンタイムに設定されているかどうかでフィルターします。
`true` の場合はワンタイムかどうかでフィルターし、`false`の場合はワンタイムでないものをフィルターします。
未指定の場合はフィルターしません。
デフォルトでは未指定です。


---
`is_disabled`  
```json
{
  "type": "boolean"
}
```
チャージQRコードが無効化されているかどうかでフィルターします。
`true` の場合は無効なものをフィルターし、`false`の場合は有効なものをフィルターします。
未指定の場合はフィルターしません。
デフォルトでは未指定です。


---
成功したときは[PaginatedChecks](#paginated-checks)オブジェクトを返します
<a name="get-check"></a>
#### チャージQRコードの表示
```typescript
const response: Response<Check> = await client.send(new GetCheck({
  check_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" // チャージQRコードのID
}));
```

---
`check_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
表示対象のチャージQRコードのIDです。

---
成功したときは[Check](#check)オブジェクトを返します
<a name="update-check"></a>
#### チャージQRコードの更新
```typescript
const response: Response<Check> = await client.send(new UpdateCheck({
  check_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // チャージQRコードのID
  money_amount: 9706.0, // 付与マネー額
  point_amount: 2136.0, // 付与ポイント額
  description: "test check", // チャージQRコードの説明文
  is_onetime: true, // ワンタイムかどうかのフラグ
  usage_limit: 7430, // ワンタイムでない場合の最大読み取り回数
  expires_at: "2020-12-10T21:14:54.000000Z", // チャージQRコード自体の失効日時
  point_expires_at: "2020-04-25T01:02:58.000000Z", // チャージQRコードによって付与されるポイント残高の有効期限
  point_expires_in_days: 60, // チャージQRコードによって付与されるポイント残高の有効期限(相対日数指定)
  bear_point_account: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // ポイント額を負担する店舗のウォレットID
  is_disabled: false // 無効化されているかどうかのフラグ
}));
```

---
`check_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
更新対象のチャージQRコードのIDです。

---
`money_amount`  
```json
{
  "type": "number",
  "format": "decimal",
  "minimum": 0
}
```
チャージQRコードによって付与されるマネー額です。
`money_amount`と`point_amount`が両方0になるような更新リクエストはエラーになります。


---
`point_amount`  
```json
{
  "type": "number",
  "format": "decimal",
  "minimum": 0
}
```
チャージQRコードによって付与されるポイント額です。
`money_amount`と`point_amount`が両方0になるような更新リクエストはエラーになります。


---
`description`  
```json
{
  "type": "string",
  "maxLength": 200
}
```
チャージQRコードの説明文です。
チャージ取引後は、取引の説明文に転記され、取引履歴などに表示されます。


---
`is_onetime`  
```json
{
  "type": "boolean"
}
```
チャージQRコードが一度の読み取りで失効するときに`true`にします。
`false`の場合、複数ユーザによって読み取り可能なQRコードになります。
ただし、その場合も1ユーザにつき1回のみしか読み取れません。


---
`usage_limit`  
```json
{
  "type": "integer"
}
```
複数ユーザによって読み取り可能なチャージQRコードの最大読み取り回数を指定します。
NULLに設定すると無制限に読み取り可能なチャージQRコードになります。
ワンタイム指定(`is_onetime`)がされているときは、本パラメータはNULLである必要があります。


---
`expires_at`  
```json
{
  "type": "string",
  "format": "date-time"
}
```
チャージQRコード自体の失効日時を指定します。この日時以降はチャージQRコードを読み取れなくなります。

チャージQRコード自体の失効日時であって、チャージQRコードによって付与されるマネー残高の有効期限とは異なることに注意してください。マネー残高の有効期限はマネー設定で指定されているものになります。


---
`point_expires_at`  
```json
{
  "type": "string",
  "format": "date-time"
}
```
チャージQRコードによって付与されるポイント残高の有効起源を指定します。

チャージQRコードにより付与されるマネー残高の有効期限はQRコード毎には指定できませんが、ポイント残高の有効期限は本パラメータにより、QRコード毎に個別に指定することができます。


---
`point_expires_in_days`  
```json
{
  "type": "integer",
  "minimum": 1
}
```
チャージQRコードによって付与されるポイント残高の有効期限を相対日数で指定します。
1を指定すると、チャージQRコード作成日の当日中に失効します(翌日0時に失効)。
`point_expires_at`と`point_expires_in_days`が両方指定されている場合は、チャージQRコードによるチャージ取引ができた時点からより近い方が採用されます。
`point_expires_at`と`point_expires_in_days`が両方NULLに設定されている場合は、マネーに設定されている残高の有効期限と同じになります。


---
`bear_point_account`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
ポイントチャージをする場合、ポイント額を負担する店舗のウォレットIDを指定することができます。


---
`is_disabled`  
```json
{
  "type": "boolean"
}
```
チャージQRコードを無効化するときに`true`にします。
`false`の場合は無効化されているチャージQRコードを再有効化します。


---
成功したときは[Check](#check)オブジェクトを返します
<a name="create-topup-transaction-with-check"></a>
#### チャージQRコードを読み取ることでチャージする
通常チャージQRコードはエンドユーザーのアプリによって読み取られ、アプリとポケペイサーバとの直接通信によって取引が作られます。 もしエンドユーザーとの通信をパートナーのサーバのみに限定したい場合、パートナーのサーバがチャージQRの情報をエンドユーザーから代理受けして、サーバ間連携APIによって実際のチャージ取引をリクエストすることになります。

エンドユーザーから受け取ったチャージ用QRコードのIDをエンドユーザーIDと共に渡すことでチャージ取引が作られます。

```typescript
const response: Response<TransactionDetail> = await client.send(new CreateTopupTransactionWithCheck({
  check_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // チャージ用QRコードのID
  customer_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // エンドユーザーのID
  request_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" // リクエストID
}));
```

---
`check_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
チャージ用QRコードのIDです。

QRコード生成時に送金元店舗のウォレット情報や、送金額などが登録されています。

---
`customer_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
エンドユーザーIDです。

送金先のエンドユーザーを指定します。

---
`request_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
取引作成APIの羃等性を担保するためのリクエスト固有のIDです。

取引作成APIで結果が受け取れなかったなどの理由で再試行する際に、二重に取引が作られてしまうことを防ぐために、クライアント側から指定されます。指定は任意で、UUID V4フォーマットでランダム生成した文字列です。リクエストIDは一定期間で削除されます。

リクエストIDを指定したとき、まだそのリクエストIDに対する取引がない場合、新規に取引が作られレスポンスとして返されます。もしそのリクエストIDに対する取引が既にある場合、既存の取引がレスポンスとして返されます。

---
成功したときは[TransactionDetail](#transaction-detail)オブジェクトを返します
### Bill
支払いQRコード
<a name="list-bills"></a>
#### 支払いQRコード一覧を表示する
支払いQRコード一覧を表示します。
```typescript
const response: Response<PaginatedBills> = await client.send(new ListBills({
  page: 6138, // ページ番号
  per_page: 8927, // 1ページの表示数
  bill_id: "T", // 支払いQRコードのID
  private_money_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // マネーID
  organization_code: "xs6VNjs2Mf2--N-VxoE9n6N1iQ3v", // 組織コード
  description: "test bill", // 取引説明文
  created_from: "2023-03-22T05:00:31.000000Z", // 作成日時(起点)
  created_to: "2024-02-06T00:24:19.000000Z", // 作成日時(終点)
  shop_name: "bill test shop1", // 店舗名
  shop_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // 店舗ID
  lower_limit_amount: 3980, // 金額の範囲によるフィルタ(下限)
  upper_limit_amount: 6980, // 金額の範囲によるフィルタ(上限)
  is_disabled: true // 支払いQRコードが無効化されているかどうか
}));
```

---
`page`  
```json
{
  "type": "integer",
  "minimum": 1
}
```
取得したいページ番号です。

---
`per_page`  
```json
{
  "type": "integer",
  "minimum": 1
}
```
1ページに表示する支払いQRコードの数です。

---
`bill_id`  
```json
{
  "type": "string"
}
```
支払いQRコードのIDを指定して検索します。IDは前方一致で検索されます。

---
`private_money_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
支払いQRコードの送金元ウォレットのマネーIDでフィルターします。

---
`organization_code`  
```json
{
  "type": "string",
  "maxLength": 32,
  "pattern": "^[a-zA-Z0-9-]*$"
}
```
支払いQRコードの送金元店舗が所属する組織の組織コードでフィルターします。

---
`description`  
```json
{
  "type": "string",
  "maxLength": 200
}
```
支払いQRコードを読み取ることで作られた取引の説明文としてアプリなどに表示されます。

---
`created_from`  
```json
{
  "type": "string",
  "format": "date-time"
}
```
支払いQRコードの作成日時でフィルターします。

これ以降に作成された支払いQRコードのみ一覧に表示されます。

---
`created_to`  
```json
{
  "type": "string",
  "format": "date-time"
}
```
支払いQRコードの作成日時でフィルターします。

これ以前に作成された支払いQRコードのみ一覧に表示されます。

---
`shop_name`  
```json
{
  "type": "string",
  "maxLength": 256
}
```
支払いQRコードを作成した店舗名でフィルターします。店舗名は部分一致で検索されます。

---
`shop_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
支払いQRコードを作成した店舗IDでフィルターします。

---
`lower_limit_amount`  
```json
{
  "type": "integer",
  "format": "decimal",
  "minimum": 0
}
```
支払いQRコードの金額の下限を指定してフィルターします。

---
`upper_limit_amount`  
```json
{
  "type": "integer",
  "format": "decimal",
  "minimum": 0
}
```
支払いQRコードの金額の上限を指定してフィルターします。

---
`is_disabled`  
```json
{
  "type": "boolean"
}
```
支払いQRコードが無効化されているかどうかを表します。デフォルト値は偽(有効)です。

---
成功したときは[PaginatedBills](#paginated-bills)オブジェクトを返します
<a name="create-bill"></a>
#### 支払いQRコードの発行
支払いQRコードの内容を更新します。支払い先の店舗ユーザーは指定したマネーのウォレットを持っている必要があります。
```typescript
const response: Response<Bill> = await client.send(new CreateBill({
  private_money_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // 支払いマネーのマネーID
  shop_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // 支払い先(受け取り人)の店舗ID
  amount: 1684.0, // 支払い額
  description: "test bill" // 説明文(アプリ上で取引の説明文として表示される)
}));
```

---
`amount`  
```json
{
  "type": "number",
  "format": "decimal",
  "minimum": 0
}
```
支払いQRコードを支払い額を指定します。省略するかnullを渡すと任意金額の支払いQRコードとなり、エンドユーザーがアプリで読み取った際に金額を入力します。

---
成功したときは[Bill](#bill)オブジェクトを返します
<a name="update-bill"></a>
#### 支払いQRコードの更新
支払いQRコードの内容を更新します。パラメータは全て省略可能で、指定したもののみ更新されます。
```typescript
const response: Response<Bill> = await client.send(new UpdateBill({
  bill_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // 支払いQRコードのID
  amount: 9656.0, // 支払い額
  description: "test bill", // 説明文
  is_disabled: true // 無効化されているかどうか
}));
```

---
`bill_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
更新対象の支払いQRコードのIDです。

---
`amount`  
```json
{
  "type": "number",
  "format": "decimal",
  "minimum": 0
}
```
支払いQRコードを支払い額を指定します。nullを渡すと任意金額の支払いQRコードとなり、エンドユーザーがアプリで読み取った際に金額を入力します。

---
`description`  
```json
{
  "type": "string",
  "maxLength": 200
}
```
支払いQRコードの詳細説明文です。アプリ上で取引の説明文として表示されます。

---
`is_disabled`  
```json
{
  "type": "boolean"
}
```
支払いQRコードが無効化されているかどうかを指定します。真にすると無効化され、偽にすると有効化します。

---
成功したときは[Bill](#bill)オブジェクトを返します
### Cashtray
Cashtrayは支払いとチャージ両方に使えるQRコードで、店舗ユーザとエンドユーザーの間の主に店頭などでの取引のために用いられます。
Cashtrayによる取引では、エンドユーザーがQRコードを読み取った時点で即時取引が作られ、ユーザに対して受け取り確認画面は表示されません。
Cashtrayはワンタイムで、一度読み取りに成功するか、取引エラーになると失効します。
また、Cashtrayには有効期限があり、デフォルトでは30分で失効します。

<a name="create-cashtray"></a>
#### Cashtrayを作る
Cashtrayを作成します。

エンドユーザーに対して支払いまたはチャージを行う店舗の情報(店舗ユーザーIDとマネーID)と、取引金額が必須項目です。
店舗ユーザーIDとマネーIDから店舗ウォレットを特定します。

その他に、Cashtrayから作られる取引に対する説明文や失効時間を指定できます。

```typescript
const response: Response<Cashtray> = await client.send(new CreateCashtray({
  private_money_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // マネーID
  shop_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // 店舗ユーザーID
  amount: 6869.0, // 金額
  description: "たい焼き(小倉)", // 取引履歴に表示する説明文
  expires_in: 3655 // 失効時間(秒)
}));
```

---
`private_money_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
取引対象のマネーのIDです(必須項目)。

---
`shop_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
店舗のユーザーIDです(必須項目)。

---
`amount`  
```json
{
  "type": "number"
}
```
マネー額です(必須項目)。
正の値を与えるとチャージになり、負の値を与えると支払いとなります。

---
`description`  
```json
{
  "type": "string",
  "maxLength": 200
}
```
Cashtrayを読み取ったときに作られる取引の説明文です(最大200文字、任意項目)。
アプリや管理画面などの取引履歴に表示されます。デフォルトでは空文字になります。

---
`expires_in`  
```json
{
  "type": "integer",
  "minimum": 1
}
```
Cashtrayが失効するまでの時間を秒単位で指定します(任意項目、デフォルト値は1800秒(30分))。

---
成功したときは[Cashtray](#cashtray)オブジェクトを返します
<a name="get-cashtray"></a>
#### Cashtrayの情報を取得する
Cashtrayの情報を取得します。

Cashtrayの現在の状態に加え、エンドユーザーのCashtray読み取りの試行結果、Cashtray読み取りによって作られた取引情報が取得できます。

レスポンス中の `attempt` には、このCashtrayをエンドユーザーが読み取った試行結果が入ります。
`account` はエンドユーザーのウォレット情報です。
成功時には `attempt` 内の `status_code` に200が入ります。

まだCashtrayが読み取られていない場合は `attempt` の内容は `NULL` になります。
エンドユーザーのCashtray読み取りの際には、様々なエラーが起き得ます。
エラーの詳細は `attempt` 中の `error_type` と `error_message` にあります。主なエラー型と対応するステータスコードを以下に列挙します。

- `cashtray_already_proceed (422)`
  - 既に処理済みのCashtrayをエンドユーザーが再び読み取ったときに返されます
- `cashtray_expired (422)`
  - 読み取り時点でCashtray自体の有効期限が切れているときに返されます。Cashtrayが失効する時刻はレスポンス中の `expires_at` にあります
- `cashtray_already_canceled (422)`
  - 読み取り時点でCashtrayが無効化されているときに返されます
- `account_balance_not_enough (422)`
  - 支払い時に、エンドユーザーの残高が不足していて取引が完了できなかったときに返されます
- `account_balance_exceeded`
  - チャージ時に、エンドユーザーのウォレット上限を超えて取引が完了できなかったときに返されます
- `account_transfer_limit_exceeded (422)`
  - マネーに設定されている一度の取引金額の上限を超えたため、取引が完了できなかったときに返されます
- `account_money_topup_transfer_limit_exceeded (422)`
  - マネーに設定されている一度のマネーチャージ金額の上限を超えたため、取引が完了できなかったときに返されます
- `account_not_found (422)`
  - Cashtrayに設定されたマネーのウォレットをエンドユーザーが持っていなかったときに返されます


レスポンス中の `transaction` には、このCashtrayをエンドユーザーが読み取ることによって作られる取引データが入ります。まだCashtrayが読み取られていない場合は `NULL` になります。

以上をまとめると、Cashtrayの状態は以下のようになります。

- エンドユーザーのCashtray読み取りによって取引が成功した場合
  - レスポンス中の `attempt` と `transaction` にそれぞれ値が入ります
- 何らかの理由で取引が失敗した場合
  - レスポンス中の `attempt` にエラー内容が入り、 `transaction` には `NULL` が入ります
- まだCashtrayが読み取られていない場合
  - レスポンス中の `attempt` と `transaction` にそれぞれ `NULL` が入ります。Cashtrayの `expires_at` が現在時刻より前の場合は有効期限切れ状態です。

Cashtrayの取り得る全ての状態を擬似コードで記述すると以下のようになります。
```
if (attempt == null) {
  // 状態は未確定
  if (canceled_at != null) {
    // 無効化済み
  } else if (expires_at < now) {
    // 失効済み
  } else {
    // まだ有効で読み取られていない
  }
} else if (transaction != null) {
  // 取引成功確定。attempt で読み取ったユーザなどが分かる
} else {
  // 取引失敗確定。attempt で失敗理由などが分かる
}
```
```typescript
const response: Response<CashtrayWithResult> = await client.send(new GetCashtray({
  cashtray_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" // CashtrayのID
}));
```

---
`cashtray_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
情報を取得するCashtrayのIDです。

---
成功したときは[CashtrayWithResult](#cashtray-with-result)オブジェクトを返します
<a name="cancel-cashtray"></a>
#### Cashtrayを無効化する
Cashtrayを無効化します。

これにより、 `GetCashtray` のレスポンス中の `canceled_at` に無効化時点での現在時刻が入るようになります。
エンドユーザーが無効化されたQRコードを読み取ると `cashtray_already_canceled` エラーとなり、取引は失敗します。
```typescript
const response: Response<Cashtray> = await client.send(new CancelCashtray({
  cashtray_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" // CashtrayのID
}));
```

---
`cashtray_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
無効化するCashtrayのIDです。

---
成功したときは[Cashtray](#cashtray)オブジェクトを返します
<a name="update-cashtray"></a>
#### Cashtrayの情報を更新する
Cashtrayの内容を更新します。bodyパラメーターは全て省略可能で、指定したもののみ更新されます。
```typescript
const response: Response<Cashtray> = await client.send(new UpdateCashtray({
  cashtray_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // CashtrayのID
  amount: 5236.0, // 金額
  description: "たい焼き(小倉)", // 取引履歴に表示する説明文
  expires_in: 6303 // 失効時間(秒)
}));
```

---
`cashtray_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
更新対象のCashtrayのIDです。

---
`amount`  
```json
{
  "type": "number"
}
```
マネー額です(任意項目)。
正の値を与えるとチャージになり、負の値を与えると支払いとなります。

---
`description`  
```json
{
  "type": "string",
  "maxLength": 200
}
```
Cashtrayを読み取ったときに作られる取引の説明文です(最大200文字、任意項目)。
アプリや管理画面などの取引履歴に表示されます。

---
`expires_in`  
```json
{
  "type": "integer",
  "minimum": 1
}
```
Cashtrayが失効するまでの時間を秒で指定します(任意項目、デフォルト値は1800秒(30分))。

---
成功したときは[Cashtray](#cashtray)オブジェクトを返します
### Customer
<a name="get-account"></a>
#### ウォレット情報を表示する
ウォレットを取得します。
```typescript
const response: Response<AccountDetail> = await client.send(new GetAccount({
  account_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" // ウォレットID
}));
```

---
`account_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
ウォレットIDです。

フィルターとして使われ、指定したウォレットIDのウォレットを取得します。

---
成功したときは[AccountDetail](#account-detail)オブジェクトを返します
<a name="update-account"></a>
#### ウォレット情報を更新する
ウォレットの状態を更新します。
以下の項目が変更できます。

- ウォレットの凍結/凍結解除の切り替え(エンドユーザー、店舗ユーザー共通)
- 店舗でチャージ可能かどうか(店舗ユーザのみ)

エンドユーザーのウォレット情報更新には UpdateCustomerAccount が使用できます。
```typescript
const response: Response<AccountDetail> = await client.send(new UpdateAccount({
  account_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // ウォレットID
  is_suspended: false, // ウォレットが凍結されているかどうか
  status: "pre-closed", // ウォレット状態
  can_transfer_topup: false // チャージ可能かどうか
}));
```

---
`account_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
ウォレットIDです。

指定したウォレットIDのウォレットの状態を更新します。

---
`is_suspended`  
```json
{
  "type": "boolean"
}
```
ウォレットの凍結状態です。真にするとウォレットが凍結され、そのウォレットでは新規取引ができなくなります。偽にすると凍結解除されます。

---
`status`  
```json
{
  "type": "string",
  "enum": [
    "active",
    "suspended",
    "pre-closed"
  ]
}
```
ウォレットの状態です。

---
`can_transfer_topup`  
```json
{
  "type": "boolean"
}
```
店舗ユーザーがエンドユーザーにチャージ可能かどうかです。真にするとチャージ可能となり、偽にするとチャージ不可能となります。

---
成功したときは[AccountDetail](#account-detail)オブジェクトを返します
<a name="delete-account"></a>
#### ウォレットを退会する
ウォレットを退会します。一度ウォレットを退会した後は、そのウォレットを再び利用可能な状態に戻すことは出来ません。
```typescript
const response: Response<AccountDeleted> = await client.send(new DeleteAccount({
  account_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // ウォレットID
  cashback: false // 返金有無
}));
```

---
`account_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
ウォレットIDです。

指定したウォレットIDのウォレットを退会します。

---
`cashback`  
```json
{
  "type": "boolean"
}
```
退会時の返金有無です。エンドユーザに返金を行う場合、真を指定して下さい。現在のマネー残高を全て現金で返金したものとして記録されます。

---
成功したときは[AccountDeleted](#account-deleted)オブジェクトを返します
<a name="list-account-balances"></a>
#### エンドユーザーの残高内訳を表示する
エンドユーザーのウォレット毎の残高を有効期限別のリストとして取得します。
```typescript
const response: Response<PaginatedAccountBalance> = await client.send(new ListAccountBalances({
  account_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // ウォレットID
  page: 6497, // ページ番号
  per_page: 6466, // 1ページ分の取引数
  expires_at_from: "2023-06-19T15:21:50.000000Z", // 有効期限の期間によるフィルター(開始時点)
  expires_at_to: "2021-03-29T13:19:12.000000Z", // 有効期限の期間によるフィルター(終了時点)
  direction: "desc" // 有効期限によるソート順序
}));
```

---
`account_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
ウォレットIDです。

フィルターとして使われ、指定したウォレットIDのウォレット残高を取得します。

---
`page`  
```json
{
  "type": "integer",
  "minimum": 1
}
```
取得したいページ番号です。デフォルト値は1です。

---
`per_page`  
```json
{
  "type": "integer",
  "minimum": 1
}
```
1ページ分のウォレット残高数です。デフォルト値は30です。

---
`expires_at_from`  
```json
{
  "type": "string",
  "format": "date-time"
}
```
有効期限の期間によるフィルターの開始時点のタイムスタンプです。デフォルトでは未指定です。

---
`expires_at_to`  
```json
{
  "type": "string",
  "format": "date-time"
}
```
有効期限の期間によるフィルターの終了時点のタイムスタンプです。デフォルトでは未指定です。

---
`direction`  
```json
{
  "type": "string",
  "enum": [
    "asc",
    "desc"
  ]
}
```
有効期限によるソートの順序を指定します。デフォルト値はasc (昇順)です。

---
成功したときは[PaginatedAccountBalance](#paginated-account-balance)オブジェクトを返します
<a name="list-account-expired-balances"></a>
#### エンドユーザーの失効済みの残高内訳を表示する
エンドユーザーのウォレット毎の失効済みの残高を有効期限別のリストとして取得します。
```typescript
const response: Response<PaginatedAccountBalance> = await client.send(new ListAccountExpiredBalances({
  account_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // ウォレットID
  page: 4131, // ページ番号
  per_page: 2277, // 1ページ分の取引数
  expires_at_from: "2023-03-19T23:33:09.000000Z", // 有効期限の期間によるフィルター(開始時点)
  expires_at_to: "2020-07-18T12:17:45.000000Z", // 有効期限の期間によるフィルター(終了時点)
  direction: "desc" // 有効期限によるソート順序
}));
```

---
`account_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
ウォレットIDです。

フィルターとして使われ、指定したウォレットIDのウォレット残高を取得します。

---
`page`  
```json
{
  "type": "integer",
  "minimum": 1
}
```
取得したいページ番号です。デフォルト値は1です。

---
`per_page`  
```json
{
  "type": "integer",
  "minimum": 1
}
```
1ページ分のウォレット残高数です。デフォルト値は30です。

---
`expires_at_from`  
```json
{
  "type": "string",
  "format": "date-time"
}
```
有効期限の期間によるフィルターの開始時点のタイムスタンプです。デフォルトでは未指定です。

---
`expires_at_to`  
```json
{
  "type": "string",
  "format": "date-time"
}
```
有効期限の期間によるフィルターの終了時点のタイムスタンプです。デフォルトでは未指定です。

---
`direction`  
```json
{
  "type": "string",
  "enum": [
    "asc",
    "desc"
  ]
}
```
有効期限によるソートの順序を指定します。デフォルト値はdesc (降順)です。

---
成功したときは[PaginatedAccountBalance](#paginated-account-balance)オブジェクトを返します
<a name="update-customer-account"></a>
#### エンドユーザーのウォレット情報を更新する
エンドユーザーのウォレットの状態を更新します。
```typescript
const response: Response<AccountWithUser> = await client.send(new UpdateCustomerAccount({
  account_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // ウォレットID
  status: "pre-closed", // ウォレット状態
  account_name: "rdqAuTxyB0A3WX2EcUb892jz3Nv10xFyFeM64iLpLDhctAZixWvzCjvZGuuLmpXAGJua2paAAkUgzb5zEsMYGbxzOIV2r2JtDEGxgzX90xQ1qEwnOjzBjMdE2ZgqC6g1ENWOPFMuygZod8nuff2bwE3RDjoGhPLmonziI8gPB410GLPQCeC7jS6W3DftZcdyglmNXEppEtAwequ", // アカウント名
  external_id: "JiYpSm0jLeVc0IIOP", // 外部ID
  metadata: "{\"key1\":\"foo\",\"key2\":\"bar\"}" // ウォレットに付加するメタデータ
}));
```

---
`account_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
ウォレットIDです。

指定したウォレットIDのウォレットの状態を更新します。

---
`status`  
```json
{
  "type": "string",
  "enum": [
    "active",
    "suspended",
    "pre-closed"
  ]
}
```
ウォレットの状態です。

---
`account_name`  
```json
{
  "type": "string",
  "maxLength": 256
}
```
変更するウォレット名です。

---
`external_id`  
```json
{
  "type": "string",
  "maxLength": 50
}
```
変更する外部IDです。

---
`metadata`  
```json
{
  "type": "string",
  "format": "json"
}
```
ウォレットに付加するメタデータをJSON文字列で指定します。
指定できるJSON文字列には以下のような制約があります。
- フラットな構造のJSONを文字列化したものであること。
- keyは最大32文字の文字列(同じkeyを複数指定することはできません)
- valueには128文字以下の文字列が指定できます

更新時に指定した内容でメタデータ全体が置き換えられることに注意してください。
例えば、元々のメタデータが以下だったときに、

'{"key1":"foo","key2":"bar"}'

更新APIで以下のように更新するとします。

'{"key1":"baz"}'

このときkey1はfooからbazに更新され、key2に対するデータは消去されます。

---
成功したときは[AccountWithUser](#account-with-user)オブジェクトを返します
<a name="get-customer-accounts"></a>
#### エンドユーザーのウォレット一覧を表示する
マネーを指定してエンドユーザーのウォレット一覧を取得します。
```typescript
const response: Response<PaginatedAccountWithUsers> = await client.send(new GetCustomerAccounts({
  private_money_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // マネーID
  page: 7999, // ページ番号
  per_page: 5598, // 1ページ分のウォレット数
  created_at_from: "2020-02-01T20:26:30.000000Z", // ウォレット作成日によるフィルター(開始時点)
  created_at_to: "2020-11-04T16:08:32.000000Z", // ウォレット作成日によるフィルター(終了時点)
  is_suspended: false, // ウォレットが凍結状態かどうかでフィルターする
  status: "suspended", // ウォレット状態
  external_id: "CcBMs9oEUXdmuJ5CsXeAgeVmz0XdBqvz2LZq", // 外部ID
  tel: "04-97-168", // エンドユーザーの電話番号
  email: "Jk1u6JVnb0@4lQy.com" // エンドユーザーのメールアドレス
}));
```

---
`private_money_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
マネーIDです。

一覧するウォレットのマネーを指定します。このパラメータは必須です。

---
`page`  
```json
{
  "type": "integer",
  "minimum": 1
}
```
取得したいページ番号です。デフォルト値は1です。

---
`per_page`  
```json
{
  "type": "integer",
  "minimum": 1
}
```
1ページ分のウォレット数です。デフォルト値は30です。

---
`created_at_from`  
```json
{
  "type": "string",
  "format": "date-time"
}
```
ウォレット作成日によるフィルターの開始時点のタイムスタンプです。デフォルトでは未指定です。

---
`created_at_to`  
```json
{
  "type": "string",
  "format": "date-time"
}
```
ウォレット作成日によるフィルターの終了時点のタイムスタンプです。デフォルトでは未指定です。

---
`is_suspended`  
```json
{
  "type": "boolean"
}
```
このパラメータが指定されている場合、ウォレットの凍結状態で結果がフィルターされます。デフォルトでは未指定です。

---
`status`  
```json
{
  "type": "string",
  "enum": [
    "active",
    "suspended",
    "pre-closed"
  ]
}
```
このパラメータが指定されている場合、ウォレットの状態で結果がフィルターされます。デフォルトでは未指定です。

---
`external_id`  
```json
{
  "type": "string",
  "maxLength": 50
}
```
外部IDでのフィルタリングです。デフォルトでは未指定です。

---
`tel`  
```json
{
  "type": "string",
  "pattern": "^0[0-9]{1,3}-?[0-9]{2,4}-?[0-9]{3,4}$"
}
```
エンドユーザーの電話番号でのフィルタリングです。デフォルトでは未指定です。

---
`email`  
```json
{
  "type": "string",
  "format": "email"
}
```
エンドユーザーのメールアドレスでのフィルタリングです。デフォルトでは未指定です。

---
成功したときは[PaginatedAccountWithUsers](#paginated-account-with-users)オブジェクトを返します
<a name="create-customer-account"></a>
#### 新規エンドユーザーをウォレットと共に追加する
指定したマネーのウォレットを作成し、同時にそのウォレットを保有するユーザも新規に作成します。
このAPIにより作成されたユーザは認証情報を持たないため、モバイルSDKやポケペイ標準アプリからはログインすることはできません。
Partner APIのみから操作可能な特殊なユーザになります。
システム全体をPartner APIのみで構成する場合にのみ使用してください。
```typescript
const response: Response<AccountWithUser> = await client.send(new CreateCustomerAccount({
  private_money_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // マネーID
  user_name: "ポケペイ太郎", // ユーザー名
  account_name: "ポケペイ太郎のアカウント", // アカウント名
  external_id: "4ktenk93ttYPJhOiPCYh" // 外部ID
}));
```

---
`private_money_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
マネーIDです。

これによって作成するウォレットのマネーを指定します。

---
`user_name`  
```json
{
  "type": "string",
  "maxLength": 256
}
```
ウォレットと共に作成するユーザ名です。省略した場合は空文字となります。

---
`account_name`  
```json
{
  "type": "string",
  "maxLength": 256
}
```
作成するウォレット名です。省略した場合は空文字となります。

---
`external_id`  
```json
{
  "type": "string",
  "maxLength": 50
}
```
PAPIクライアントシステムから利用するPokepayユーザーのIDです。デフォルトでは未指定です。

---
成功したときは[AccountWithUser](#account-with-user)オブジェクトを返します
<a name="get-shop-accounts"></a>
#### 店舗ユーザーのウォレット一覧を表示する
マネーを指定して店舗ユーザーのウォレット一覧を取得します。
```typescript
const response: Response<PaginatedAccountWithUsers> = await client.send(new GetShopAccounts({
  private_money_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // マネーID
  page: 3879, // ページ番号
  per_page: 362, // 1ページ分のウォレット数
  created_at_from: "2022-12-20T22:26:04.000000Z", // ウォレット作成日によるフィルター(開始時点)
  created_at_to: "2024-02-05T20:41:24.000000Z", // ウォレット作成日によるフィルター(終了時点)
  is_suspended: false // ウォレットが凍結状態かどうかでフィルターする
}));
```

---
`private_money_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
マネーIDです。

一覧するウォレットのマネーを指定します。このパラメータは必須です。

---
`page`  
```json
{
  "type": "integer",
  "minimum": 1
}
```
取得したいページ番号です。デフォルト値は1です。

---
`per_page`  
```json
{
  "type": "integer",
  "minimum": 1
}
```
1ページ分のウォレット数です。デフォルト値は30です。

---
`created_at_from`  
```json
{
  "type": "string",
  "format": "date-time"
}
```
ウォレット作成日によるフィルターの開始時点のタイムスタンプです。デフォルトでは未指定です。

---
`created_at_to`  
```json
{
  "type": "string",
  "format": "date-time"
}
```
ウォレット作成日によるフィルターの終了時点のタイムスタンプです。デフォルトでは未指定です。

---
`is_suspended`  
```json
{
  "type": "boolean"
}
```
このパラメータが指定されている場合、ウォレットの凍結状態で結果がフィルターされます。デフォルトでは未指定です。

---
成功したときは[PaginatedAccountWithUsers](#paginated-account-with-users)オブジェクトを返します
<a name="list-customer-transactions"></a>
#### 取引履歴を取得する
取引一覧を返します。
```typescript
const response: Response<PaginatedTransaction> = await client.send(new ListCustomerTransactions({
  private_money_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // マネーID
  sender_customer_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // 送金エンドユーザーID
  receiver_customer_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // 受取エンドユーザーID
  type: "expire", // 取引種別
  is_modified: false, // キャンセル済みかどうか
  from: "2023-10-17T16:01:34.000000Z", // 開始日時
  to: "2022-11-24T21:29:52.000000Z", // 終了日時
  page: 1, // ページ番号
  per_page: 50 // 1ページ分の取引数
}));
```

---
`private_money_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
マネーIDです。
フィルターとして使われ、指定したマネーでの取引のみ一覧に表示されます。

---
`sender_customer_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
送金ユーザーIDです。

フィルターとして使われ、指定された送金ユーザーでの取引のみ一覧に表示されます。

---
`receiver_customer_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
受取ユーザーIDです。

フィルターとして使われ、指定された受取ユーザーでの取引のみ一覧に表示されます。

---
`type`  
```json
{
  "type": "string",
  "enum": [
    "topup",
    "payment",
    "exchange",
    "transfer",
    "cashback",
    "expire"
  ]
}
```
取引の種類でフィルターします。

以下の種類を指定できます。

1. topup
   店舗からエンドユーザーへの送金取引(チャージ)
2. payment
   エンドユーザーから店舗への送金取引(支払い)
3. exchange
   他マネーへの流出(outflow)/他マネーからの流入(inflow)
4. transfer
   個人間送金
5. cashback
   ウォレット退会時返金
6. expire
   ウォレット退会時失効

---
`is_modified`  
```json
{
  "type": "boolean"
}
```
キャンセル済みかどうかを判定するフラグです。

これにtrueを指定するとキャンセルされた取引のみ一覧に表示されます。
falseを指定するとキャンセルされていない取引のみ一覧に表示されます
何も指定しなければキャンセルの有無にかかわらず一覧に表示されます。

---
`from`  
```json
{
  "type": "string",
  "format": "date-time"
}
```
抽出期間の開始日時です。

フィルターとして使われ、開始日時以降に発生した取引のみ一覧に表示されます。

---
`to`  
```json
{
  "type": "string",
  "format": "date-time"
}
```
抽出期間の終了日時です。

フィルターとして使われ、終了日時以前に発生した取引のみ一覧に表示されます。

---
`page`  
```json
{
  "type": "integer",
  "minimum": 1
}
```
取得したいページ番号です。

---
`per_page`  
```json
{
  "type": "integer",
  "minimum": 1
}
```
1ページ分の取引数です。

---
成功したときは[PaginatedTransaction](#paginated-transaction)オブジェクトを返します
### Organization
<a name="list-organizations"></a>
#### 加盟店組織の一覧を取得する
```typescript
const response: Response<PaginatedOrganizations> = await client.send(new ListOrganizations({
  private_money_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // マネーID
  page: 1, // ページ番号
  per_page: 50, // 1ページ分の取引数
  name: "teZ9v4lYI", // 組織名
  code: "rYpnV35" // 組織コード
}));
```

---
`private_money_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
マネーIDです。
このマネーに加盟している加盟組織がフィルターされます。

---
`page`  
```json
{
  "type": "integer",
  "minimum": 1
}
```
取得したいページ番号です。

---
`per_page`  
```json
{
  "type": "integer",
  "minimum": 1
}
```
1ページ分の取引数です。

---
成功したときは[PaginatedOrganizations](#paginated-organizations)オブジェクトを返します
<a name="create-organization"></a>
#### 新規加盟店組織を追加する
```typescript
const response: Response<Organization> = await client.send(new CreateOrganization({
  code: "ox-supermarket", // 新規組織コード
  name: "oxスーパー", // 新規組織名
  private_money_ids: ["xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"], // 加盟店組織で有効にするマネーIDの配列
  issuer_admin_user_email: "pBMGKJEJkp@n6Ml.com", // 発行体担当者メールアドレス
  member_admin_user_email: "r99tmpLoTF@QeHI.com", // 新規組織担当者メールアドレス
  bank_name: "XYZ銀行", // 銀行名
  bank_code: "1234", // 銀行金融機関コード
  bank_branch_name: "ABC支店", // 銀行支店名
  bank_branch_code: "123", // 銀行支店コード
  bank_account_type: "saving", // 銀行口座種別 (普通=saving, 当座=current, その他=other)
  bank_account: "1234567", // 銀行口座番号
  bank_account_holder_name: "ﾌｸｻﾞﾜﾕｷﾁ", // 口座名義人名
  contact_name: "佐藤清" // 担当者名
}));
```
成功したときは[Organization](#organization)オブジェクトを返します
### Shop
<a name="list-shops"></a>
#### 店舗一覧を取得する
```typescript
const response: Response<PaginatedShops> = await client.send(new ListShops({
  organization_code: "pocketchange", // 組織コード
  private_money_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // マネーID
  name: "oxスーパー三田店", // 店舗名
  postal_code: "3992548", // 店舗の郵便番号
  address: "東京都港区芝...", // 店舗の住所
  tel: "04-018-143", // 店舗の電話番号
  email: "3zE32Vk24C@een1.com", // 店舗のメールアドレス
  external_id: "SjytDUp3byZcFEP", // 店舗の外部ID
  with_disabled: true, // 無効な店舗を含める
  page: 1, // ページ番号
  per_page: 50 // 1ページ分の取引数
}));
```

---
`organization_code`  
```json
{
  "type": "string",
  "maxLength": 32,
  "pattern": "^[a-zA-Z0-9-]*$"
}
```
このパラメータを渡すとその組織の店舗のみが返され、省略すると加盟店も含む店舗が返されます。


---
`private_money_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
このパラメータを渡すとそのマネーのウォレットを持つ店舗のみが返されます。


---
`name`  
```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 256
}
```
このパラメータを渡すとその名前の店舗のみが返されます。


---
`postal_code`  
```json
{
  "type": "string",
  "pattern": "^[0-9]{3}-?[0-9]{4}$"
}
```
このパラメータを渡すとその郵便番号が登録された店舗のみが返されます。


---
`address`  
```json
{
  "type": "string",
  "maxLength": 256
}
```
このパラメータを渡すとその住所が登録された店舗のみが返されます。


---
`tel`  
```json
{
  "type": "string",
  "pattern": "^0[0-9]{1,3}-?[0-9]{2,4}-?[0-9]{3,4}$"
}
```
このパラメータを渡すとその電話番号が登録された店舗のみが返されます。


---
`email`  
```json
{
  "type": "string",
  "format": "email",
  "maxLength": 256
}
```
このパラメータを渡すとそのメールアドレスが登録された店舗のみが返されます。


---
`external_id`  
```json
{
  "type": "string",
  "maxLength": 36
}
```
このパラメータを渡すとその外部IDが登録された店舗のみが返されます。


---
`with_disabled`  
```json
{
  "type": "boolean"
}
```
このパラメータを渡すと無効にされた店舗を含めて返されます。デフォルトでは無効にされた店舗は返されません。


---
`page`  
```json
{
  "type": "integer",
  "minimum": 1
}
```
取得したいページ番号です。

---
`per_page`  
```json
{
  "type": "integer",
  "minimum": 1
}
```
1ページ分の取引数です。

---
成功したときは[PaginatedShops](#paginated-shops)オブジェクトを返します
<a name="create-shop"></a>
#### 【廃止】新規店舗を追加する
新規店舗を追加します。このAPIは廃止予定です。以降は `CreateShopV2` を使用してください。
```typescript
const response: Response<User> = await client.send(new CreateShop({
  shop_name: "oxスーパー三田店", // 店舗名
  shop_postal_code: "946-7553", // 店舗の郵便番号
  shop_address: "東京都港区芝...", // 店舗の住所
  shop_tel: "01918-7038", // 店舗の電話番号
  shop_email: "JaXsPvnXy7@JLPW.com", // 店舗のメールアドレス
  shop_external_id: "4POJKIKUBKfvAdAdVhR8q", // 店舗の外部ID
  organization_code: "ox-supermarket" // 組織コード
}));
```
成功したときは[User](#user)オブジェクトを返します
<a name="create-shop-v2"></a>
#### 新規店舗を追加する
```typescript
const response: Response<ShopWithAccounts> = await client.send(new CreateShopV2({
  name: "oxスーパー三田店", // 店舗名
  postal_code: "670-5440", // 店舗の郵便番号
  address: "東京都港区芝...", // 店舗の住所
  tel: "0831214078", // 店舗の電話番号
  email: "zOOhzPjoLU@npes.com", // 店舗のメールアドレス
  external_id: "4zWmpVcy9ixDX4fCfbAE0A", // 店舗の外部ID
  organization_code: "ox-supermarket", // 組織コード
  private_money_ids: ["xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"], // 店舗で有効にするマネーIDの配列
  can_topup_private_money_ids: [] // 店舗でチャージ可能にするマネーIDの配列
}));
```

---
`name`  
```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 256
}
```
店舗名です。

同一組織内に同名の店舗があった場合は`name_conflict`エラーが返ります。

---
`private_money_ids`  
```json
{
  "type": "array",
  "minItems": 1,
  "items": {
    "type": "string",
    "format": "uuid"
  }
}
```
店舗で有効にするマネーIDの配列を指定します。

店舗が所属する組織が発行または加盟しているマネーのみが指定できます。利用できないマネーが指定された場合は`unavailable_private_money`エラーが返ります。
このパラメータを省略したときは、店舗が所属する組織が発行または加盟している全てのマネーのウォレットができます。

---
`can_topup_private_money_ids`  
```json
{
  "type": "array",
  "minItems": 0,
  "items": {
    "type": "string",
    "format": "uuid"
  }
}
```
店舗でチャージ可能にするマネーIDの配列を指定します。

このパラメータは発行体のみが指定でき、自身が発行しているマネーのみを指定できます。加盟店が他発行体のマネーに加盟している場合でも、そのチャージ可否を変更することはできません。
省略したときは対象店舗のその発行体の全てのマネーのアカウントがチャージ不可となります。

---
成功したときは[ShopWithAccounts](#shop-with-accounts)オブジェクトを返します
<a name="get-shop"></a>
#### 店舗情報を表示する
店舗情報を表示します。

権限に関わらず自組織の店舗情報は表示可能です。それに加え、発行体は自組織の発行しているマネーの加盟店組織の店舗情報を表示できます。
```typescript
const response: Response<ShopWithAccounts> = await client.send(new GetShop({
  shop_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" // 店舗ユーザーID
}));
```
成功したときは[ShopWithAccounts](#shop-with-accounts)オブジェクトを返します
<a name="update-shop"></a>
#### 店舗情報を更新する
店舗情報を更新します。bodyパラメーターは全て省略可能で、指定したもののみ更新されます。
```typescript
const response: Response<ShopWithAccounts> = await client.send(new UpdateShop({
  shop_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // 店舗ユーザーID
  name: "oxスーパー三田店", // 店舗名
  postal_code: "804-8661", // 店舗の郵便番号
  address: "東京都港区芝...", // 店舗の住所
  tel: "01-35872", // 店舗の電話番号
  email: "DuJC7DFGXW@J1Ds.com", // 店舗のメールアドレス
  external_id: "LyOnXTqwNlXWPSNst44xBM1tMMoOy", // 店舗の外部ID
  private_money_ids: ["xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"], // 店舗で有効にするマネーIDの配列
  can_topup_private_money_ids: ["xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"], // 店舗でチャージ可能にするマネーIDの配列
  status: "disabled" // 店舗の状態
}));
```

---
`name`  
```json
{
  "type": "string",
  "minLength": 1,
  "maxLength": 256
}
```
店舗名です。

同一組織内に同名の店舗があった場合は`shop_name_conflict`エラーが返ります。

---
`postal_code`  
```json
{
  "type": "string",
  "pattern": "^[0-9]{3}-?[0-9]{4}$"
}
```
店舗住所の郵便番号(7桁の数字)です。ハイフンは無視されます。明示的に空の値を設定するにはNULLを指定します。

---
`tel`  
```json
{
  "type": "string",
  "pattern": "^0[0-9]{1,3}-?[0-9]{2,4}-?[0-9]{3,4}$"
}
```
店舗の電話番号です。ハイフンは無視されます。明示的に空の値を設定するにはNULLを指定します。

---
`email`  
```json
{
  "type": "string",
  "format": "email",
  "maxLength": 256
}
```
店舗の連絡先メールアドレスです。明示的に空の値を設定するにはNULLを指定します。

---
`external_id`  
```json
{
  "type": "string",
  "maxLength": 36
}
```
店舗の外部IDです(最大36文字)。明示的に空の値を設定するにはNULLを指定します。

---
`private_money_ids`  
```json
{
  "type": "array",
  "minItems": 0,
  "items": {
    "type": "string",
    "format": "uuid"
  }
}
```
店舗で有効にするマネーIDの配列を指定します。

店舗が所属する組織が発行または加盟しているマネーのみが指定できます。利用できないマネーが指定された場合は`unavailable_private_money`エラーが返ります。
店舗が既にウォレットを持っている場合に、ここでそのウォレットのマネーIDを指定しないで更新すると、そのマネーのウォレットは凍結(無効化)されます。

---
`can_topup_private_money_ids`  
```json
{
  "type": "array",
  "minItems": 0,
  "items": {
    "type": "string",
    "format": "uuid"
  }
}
```
店舗でチャージ可能にするマネーIDの配列を指定します。

このパラメータは発行体のみが指定でき、発行しているマネーのみを指定できます。加盟店が他発行体のマネーに加盟している場合でも、そのチャージ可否を変更することはできません。
省略したときは対象店舗のその発行体の全てのマネーのアカウントがチャージ不可となります。

---
`status`  
```json
{
  "type": "string",
  "enum": [
    "active",
    "disabled"
  ]
}
```
店舗の状態です。activeを指定すると有効となり、disabledを指定するとリスト表示から除外されます。

---
成功したときは[ShopWithAccounts](#shop-with-accounts)オブジェクトを返します
### Account
<a name="list-user-accounts"></a>
#### エンドユーザー、店舗ユーザーのウォレット一覧を表示する
ユーザーIDを指定してそのユーザーのウォレット一覧を取得します。
```typescript
const response: Response<PaginatedAccountDetails> = await client.send(new ListUserAccounts({
  user_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // ユーザーID
  page: 4395, // ページ番号
  per_page: 5442 // 1ページ分の取引数
}));
```

---
`user_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
ユーザーIDです。

指定したユーザーIDのウォレット一覧を取得します。パートナーキーと紐づく組織が発行しているマネーのウォレットのみが表示されます。

---
`page`  
```json
{
  "type": "integer",
  "minimum": 1
}
```
取得したいページ番号です。デフォルト値は1です。

---
`per_page`  
```json
{
  "type": "integer",
  "minimum": 1
}
```
1ページ当たりのウォレット数です。デフォルト値は50です。

---
成功したときは[PaginatedAccountDetails](#paginated-account-details)オブジェクトを返します
<a name="create-user-account"></a>
#### エンドユーザーのウォレットを作成する
既存のエンドユーザーに対して、指定したマネーのウォレットを新規作成します
```typescript
const response: Response<AccountDetail> = await client.send(new CreateUserAccount({
  user_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // ユーザーID
  private_money_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // マネーID
  name: "qWcD5ADFBSPh7o2MC5sMNAQhF0HCoj9Dj4ZpJqp2buSHK5WKI86hTWo47qb9nSKNBR3LjzCdQo4GwTY7y2Am8ZcyGh3BczuQ1HmAT4U7cCHORIBupKF2LGLWlWRqEU1R3HVfumJrkxA1RBhkJnrKn6T4", // ウォレット名
  external_id: "UBYf7XzEp3cMOeoQItbJApNFN", // 外部ID
  metadata: "{\"key1\":\"foo\",\"key2\":\"bar\"}" // ウォレットに付加するメタデータ
}));
```

---
`user_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
ユーザーIDです。

---
`private_money_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
マネーIDです。

作成するウォレットのマネーを指定します。このパラメータは必須です。

---
`metadata`  
```json
{
  "type": "string",
  "format": "json"
}
```
ウォレットに付加するメタデータをJSON文字列で指定します。
指定できるJSON文字列には以下のような制約があります。
- フラットな構造のJSONを文字列化したものであること。
- keyは最大32文字の文字列(同じkeyを複数指定することはできません)
- valueには128文字以下の文字列が指定できます

---
成功したときは[AccountDetail](#account-detail)オブジェクトを返します
### Private Money
<a name="get-private-moneys"></a>
#### マネー一覧を取得する
マネーの一覧を取得します。
パートナーキーの管理者が発行体組織に属している場合、自組織が加盟または発行しているマネーの一覧を返します。また、`organization_code`として決済加盟店の組織コードを指定した場合、発行マネーのうち、その決済加盟店組織が加盟しているマネーの一覧を返します。
パートナーキーの管理者が決済加盟店組織に属している場合は、自組織が加盟しているマネーの一覧を返します。
```typescript
const response: Response<PaginatedPrivateMoneys> = await client.send(new GetPrivateMoneys({
  organization_code: "ox-supermarket", // 組織コード
  page: 1, // ページ番号
  per_page: 50 // 1ページ分の取得数
}));
```

---
`organization_code`  
```json
{
  "type": "string",
  "maxLength": 32,
  "pattern": "^[a-zA-Z0-9-]*$"
}
```
パートナーキーの管理者が発行体組織に属している場合、発行マネーのうち、この組織コードで指定した決済加盟店組織が加盟しているマネーの一覧を返します。決済加盟店組織の管理者は自組織以外を指定することはできません。

---
成功したときは[PaginatedPrivateMoneys](#paginated-private-moneys)オブジェクトを返します
<a name="get-private-money-organization-summaries"></a>
#### 決済加盟店の取引サマリを取得する
```typescript
const response: Response<PaginatedPrivateMoneyOrganizationSummaries> = await client.send(new GetPrivateMoneyOrganizationSummaries({
  private_money_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // マネーID
  from: "2020-09-18T02:56:34.000000Z", // 開始日時(toと同時に指定する必要有)
  to: "2021-10-07T06:02:17.000000Z", // 終了日時(fromと同時に指定する必要有)
  page: 1, // ページ番号
  per_page: 50 // 1ページ分の取引数
}));
```
`from`と`to`は同時に指定する必要があります。

成功したときは[PaginatedPrivateMoneyOrganizationSummaries](#paginated-private-money-organization-summaries)オブジェクトを返します
<a name="get-private-money-summary"></a>
#### 取引サマリを取得する
```typescript
const response: Response<PrivateMoneySummary> = await client.send(new GetPrivateMoneySummary({
  private_money_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // マネーID
  from: "2020-01-01T00:02:02.000000Z", // 開始日時
  to: "2020-06-08T05:00:33.000000Z" // 終了日時
}));
```
成功したときは[PrivateMoneySummary](#private-money-summary)オブジェクトを返します
### Bulk
<a name="bulk-create-transaction"></a>
#### CSVファイル一括取引
CSVファイルから一括取引をします。
```typescript
const response: Response<BulkTransaction> = await client.send(new BulkCreateTransaction({
  name: "SEKvNBsiLTmRsG1pcvzP", // 一括取引タスク名
  content: "SNlMjgy", // 取引する情報のCSV
  request_id: "Cm3l36NNuyyweAXXanZiLS6lbj9JXoVWEOjN", // リクエストID
  description: "WcJ8Pqob8ZB", // 一括取引の説明
  private_money_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" // マネーID
}));
```

---
`name`  
```json
{
  "type": "string",
  "maxLength": 32
}
```
一括取引タスクの管理用の名前です。

---
`description`  
```json
{
  "type": "string",
  "maxLength": 128
}
```
一括取引タスクの管理用の説明文です。

---
`content`  
```json
{
  "type": "string"
}
```
一括取引する情報を書いたCSVの文字列です。
1行目はヘッダ行で、2行目以降の各行にカンマ区切りの取引データを含みます。
カラムは以下の7つです。任意のカラムには空文字を指定します。

- `type`: 取引種別
  - 必須。'topup' または 'payment'
- `sender_id`: 送金ユーザーID
  - 必須。UUID
- `receiver_id`: 受取ユーザーID
  - 必須。UUID
- `private_money_id`: マネーID
  - 必須。UUID
- `money_amount`: マネー額
  - 任意。ただし `point_amount` といずれかが必須。0以上の数字
- `point_amount`: ポイント額
  - 任意。ただし `money_amount` といずれかが必須。0以上の数字
- `description`: 取引の説明文
  - 任意。200文字以内。取引履歴に表示される文章
- `bear_account_id`: ポイント負担ウォレットID
  - `point_amount` があるときは必須。UUID
- `point_expires_at`: ポイントの有効期限
  - 任意。指定がないときはマネーに設定された有効期限を適用

---
`request_id`  
```json
{
  "type": "string",
  "minLength": 36,
  "maxLength": 36
}
```
重複したリクエストを判断するためのユニークID。ランダムな36字の文字列を生成して渡してください。

---
`private_money_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
マネーIDです。 マネーを指定します。

---
成功したときは[BulkTransaction](#bulk-transaction)オブジェクトを返します
### Event
<a name="create-external-transaction"></a>
#### ポケペイ外部取引を作成する
ポケペイ外部取引を作成します。

ポケペイ外の現金決済やクレジットカード決済に対してポケペイのポイントを付けたいというときに使用します。

```typescript
const response: Response<ExternalTransactionDetail> = await client.send(new CreateExternalTransaction({
  shop_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // 店舗ID
  customer_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // エンドユーザーID
  private_money_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // マネーID
  amount: 129, // 取引額
  description: "たい焼き(小倉)", // 取引説明文
  metadata: "{\"key\":\"value\"}", // ポケペイ外部取引メタデータ
  products: [{"jan_code":"abc",
 "name":"name1",
 "unit_price":100,
 "price": 100,
 "is_discounted": false,
 "other":"{}"}], // 商品情報データ
  request_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" // リクエストID
}));
```

---
`shop_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
店舗IDです。

ポケペイ外部取引が行なう店舗を指定します。

---
`customer_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
エンドユーザーIDです。

エンドユーザーを指定します。

---
`private_money_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
マネーIDです。

マネーを指定します。

---
`amount`  
```json
{
  "type": "integer",
  "minimum": 0
}
```
取引金額です。

---
`description`  
```json
{
  "type": "string",
  "maxLength": 200
}
```
取引説明文です。

任意入力で、取引履歴に表示される説明文です。

---
`metadata`  
```json
{
  "type": "string",
  "format": "json"
}
```
ポケペイ外部取引作成時に指定され、取引と紐付けられるメタデータです。

任意入力で、全てのkeyとvalueが文字列であるようなフラットな構造のJSONで指定します。

---
`products`  
```json
{
  "type": "array",
  "items": {
    "type": "object"
  }
}
```
一つの取引に含まれる商品情報データです。
以下の内容からなるJSONオブジェクトの配列で指定します。

- `jan_code`: JANコード。64字以下の文字列
- `name`: 商品名。256字以下の文字列
- `unit_price`: 商品単価。0以上の数値
- `price`: 全体の金額(例: 商品単価 × 個数)。0以上の数値
- `is_discounted`: 賞味期限が近いなどの理由で商品が値引きされているかどうかのフラグ。boolean
- `other`: その他商品に関する情報。JSONオブジェクトで指定します。

---
`request_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
取引作成APIの羃等性を担保するためのリクエスト固有のIDです。

取引作成APIで結果が受け取れなかったなどの理由で再試行する際に、二重に取引が作られてしまうことを防ぐために、クライアント側から指定されます。指定は任意で、UUID V4フォーマットでランダム生成した文字列です。リクエストIDは一定期間で削除されます。

リクエストIDを指定したとき、まだそのリクエストIDに対する取引がない場合、新規に取引が作られレスポンスとして返されます。もしそのリクエストIDに対する取引が既にある場合、既存の取引がレスポンスとして返されます。

---
成功したときは[ExternalTransactionDetail](#external-transaction-detail)オブジェクトを返します
<a name="refund-external-transaction"></a>
#### ポケペイ外部取引をキャンセルする
取引IDを指定して取引をキャンセルします。

発行体の管理者は自組織の直営店、または発行しているマネーの決済加盟店組織での取引をキャンセルできます。
キャンセル対象のポケペイ外部取引に付随するポイント還元キャンペーンも取り消されます。

取引をキャンセルできるのは1回きりです。既にキャンセルされた取引を重ねてキャンセルしようとすると `transaction_already_refunded (422)` エラーが返ります。
```typescript
const response: Response<ExternalTransactionDetail> = await client.send(new RefundExternalTransaction({
  event_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // 取引ID
  description: "返品対応のため" // 取引履歴に表示する返金事由
}));
```
成功したときは[ExternalTransactionDetail](#external-transaction-detail)オブジェクトを返します
### Campaign
<a name="create-campaign"></a>
#### ポイント付与キャンペーンを作る
ポイント付与キャンペーンを作成します。

```typescript
const response: Response<Campaign> = await client.send(new CreateCampaign({
  name: "c2LIkAJFpX3tMiPvkskrBs7cZNQht6pUXt6QkeG9pRp1c5EcN6nLJcb0NEcuMnzKSDbJD", // キャンペーン名
  private_money_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // マネーID
  starts_at: "2020-05-30T05:04:19.000000Z", // キャンペーン開始日時
  ends_at: "2022-08-14T15:51:01.000000Z", // キャンペーン終了日時
  priority: 843, // キャンペーンの適用優先度
  event: "external-transaction", // イベント種別
  bear_point_shop_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // ポイント負担先店舗ID
  description: "yRniwPaN0afN8mRVY0r2kLaYAQQnNWq5gJk8ucSDE2uEYUD0C3IXLL4lH8T3KxBkSfET7NeTYdPy8UjYc9OlslQQZIq7zSOEeSzczj6ObIBdQwmJP2q6udBME6WRlyybO27figMsVR", // キャンペーンの説明文
  status: "enabled", // キャンペーン作成時の状態
  point_expires_at: "2022-11-20T05:16:21.000000Z", // ポイント有効期限(絶対日時指定)
  point_expires_in_days: 4544, // ポイント有効期限(相対日数指定)
  is_exclusive: true, // キャンペーンの重複設定
  subject: "all", // ポイント付与の対象金額の種別
  amount_based_point_rules: [{
  "point_amount": 5,
  "point_amount_unit": "percent",
  "subject_more_than_or_equal": 1000,
  "subject_less_than": 5000
}], // 取引金額ベースのポイント付与ルール
  product_based_point_rules: [{
  "point_amount": 5,
  "point_amount_unit": "percent",
  "product_code": "4912345678904",
  "is_multiply_by_count": true,
  "required_count": 2
}], // 商品情報ベースのポイント付与ルール
  applicable_days_of_week: [5, 6, 4], // キャンペーンを適用する曜日 (複数指定)
  applicable_time_ranges: [{
  "from": "12:00",
  "to": "23:59"
}, {
  "from": "12:00",
  "to": "23:59"
}], // キャンペーンを適用する時間帯 (複数指定)
  applicable_shop_ids: ["xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"], // キャンペーン適用対象となる店舗IDのリスト
  minimum_number_for_combination_purchase: 6166, // 複数種類の商品を同時購入するときの商品種別数の下限
  exist_in_each_product_groups: true, // 複数の商品グループにつき1種類以上の商品購入によって発火するキャンペーンの指定フラグ
  max_point_amount: 134, // キャンペーンによって付与されるポイントの上限
  max_total_point_amount: 9447, // キャンペーンによって付与されるの1人当たりの累計ポイントの上限
  dest_private_money_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // ポイント付与先となるマネーID
  applicable_account_metadata: {
  "key": "sex",
  "value": "male"
}, // ウォレットに紐付くメタデータが特定の値を持つときにのみ発火するキャンペーンを登録します。
  budget_caps_amount: 422935798 // キャンペーン予算上限
}));
```

---
`name`  
```json
{
  "type": "string",
  "maxLength": 256
}
```
キャンペーン名です(必須項目)。

ポイント付与によってできるチャージ取引の説明文に転記されます。取引説明文はエンドユーザーからも確認できます。

---
`private_money_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
キャンペーン対象のマネーのIDです(必須項目)。

---
`starts_at`  
```json
{
  "type": "string",
  "format": "date-time"
}
```
キャンペーン開始日時です(必須項目)。
キャンペーン期間中のみポイントが付与されます。
開始日時よりも終了日時が前のときはcampaign_invalid_periodエラー(422)になります。

---
`ends_at`  
```json
{
  "type": "string",
  "format": "date-time"
}
```
キャンペーン終了日時です(必須項目)。
キャンペーン期間中のみポイントが付与されます。
開始日時よりも終了日時が前のときはcampaign_invalid_periodエラー(422)になります。

---
`priority`  
```json
{
  "type": "integer"
}
```
キャンペーンの適用優先度です。

優先度が大きいものから順に適用判定されていきます。
キャンペーン期間が重なっている同一の優先度のキャンペーンが存在するとcampaign_period_overlapsエラー(422)になります。

---
`event`  
```json
{
  "type": "string",
  "enum": [
    "topup",
    "payment",
    "external-transaction"
  ]
}
```
キャンペーンのトリガーとなるイベントの種類を指定します(必須項目)。

以下のいずれかを指定できます。

1. topup
   店舗からエンドユーザーへの送金取引(チャージ)
2. payment
   エンドユーザーから店舗への送金取引(支払い)
3. external-transaction
   ポケペイ外の取引(現金決済など)

---
`bear_point_shop_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
ポイントを負担する店舗のIDです。デフォルトではマネー発行体の本店が設定されます。
ポイント負担先店舗は後から更新することはできません。

---
`description`  
```json
{
  "type": "string",
  "maxLength": 200
}
```
キャンペーンの内容を記載します。管理画面などでキャンペーンを管理するための説明文になります。

---
`status`  
```json
{
  "type": "string",
  "enum": [
    "enabled",
    "disabled"
  ]
}
```
キャンペーン作成時の状態を指定します。デフォルトではenabledです。

以下のいずれかを指定できます。

1. enabled
   有効
2. disabled
   無効

---
`point_expires_at`  
```json
{
  "type": "string",
  "format": "date-time"
}
```
キャンペーンによって付与されるポイントの有効期限を絶対日時で指定します。
省略した場合はマネーに設定された有効期限と同じものがポイントの有効期限となります。

---
`point_expires_in_days`  
```json
{
  "type": "integer",
  "minimum": 1
}
```
キャンペーンによって付与されるポイントの有効期限を相対日数で指定します。
省略した場合はマネーに設定された有効期限と同じものがポイントの有効期限となります。

---
`is_exclusive`  
```json
{
  "type": "boolean"
}
```
キャンペーンの重ね掛けを行うかどうかのフラグです。

これにtrueを指定すると他のキャンペーンと同時適用されません。デフォルト値はtrueです。
falseを指定すると次の優先度の重ね掛け可能なキャンペーンの適用判定に進みます。

---
`subject`  
```json
{
  "type": "string",
  "enum": [
    "money",
    "all"
  ]
}
```
ポイント付与額を計算する対象となる金額の種類を指定します。デフォルト値はallです。
eventとしてexternal-transactionを指定した場合はポイントとマネーの区別がないためsubjectの指定に関わらず常にallとなります。

以下のいずれかを指定できます。

1. money
moneyを指定すると決済額の中で「マネー」を使って支払った額を対象にします

2. all
all を指定すると決済額全体を対象にします (「ポイント」での取引額を含む)
注意: event を topup にしたときはポイントの付与に対しても適用されます

---
`amount_based_point_rules`  
```json
{
  "type": "array",
  "items": {
    "type": "object"
  }
}
```
金額をベースとしてポイント付与を行うルールを指定します。
amount_based_point_rules と product_based_point_rules はどちらか一方しか指定できません。
各ルールは一つのみ適用され、条件に重複があった場合は先に記載されたものが優先されます。

例:
```javascript
[
  // 1000円以上、5000円未満の決済には 5％
  {
    "point_amount": 5,
    "point_amount_unit": "percent",
    "subject_more_than_or_equal": 1000,
    "subject_less_than": 5000
  },
  // 5000円以上の決済には 10%
  {
    "point_amount": 10,
    "point_amount_unit": "percent",
    "subject_more_than_or_equal": 5000
  },
]
```

---
`product_based_point_rules`  
```json
{
  "type": "array",
  "items": {
    "type": "object"
  }
}
```
商品情報をベースとしてポイント付与を行うルールを指定します。
ルールは商品ごとに設定可能で、ルールの配列として指定します。
amount_based_point_rules と product_based_point_rules はどちらか一方しか指定できません。
event が payment か external-transaction の時のみ有効です。
各ルールの順序は問わず、適用可能なものは全て適用されます。
一つの決済の中で複数の商品がキャンペーン適用可能な場合はそれぞれの商品についてのルールが適用され、ポイント付与額はその合算になります。

例:
```javascript
[
  // 対象商品の購入額から5%ポイント付与。複数購入時は単価の5%が付与される。
  {
    "point_amount": 5,
    "point_amount_unit": "percent",
    "product_code": "4912345678904",
  },
  // 対象商品の購入額から5%ポイント付与。複数購入時は購入総額の5%が付与される。
  {
    "point_amount": 5,
    "point_amount_unit": "percent",
    "product_code": "4912345678904",
    "is_multiply_by_count": true,
  },
  // 対象商品を2つ以上購入したら500ポイント付与(固定額付与)
  {
    "point_amount": 500,
    "point_amount_unit": "absolute",
    "product_code": "4912345678904",
    "required_count": 2
  },
  // 書籍は10%ポイント付与
  // ※ISBNの形式はレジがポケペイに送信する形式に準じます
  {
    "point_amount": 10,
    "point_amount_unit": "percent",
    "product_code": "978-%",
  },
  // 一部の出版社の書籍は10%ポイント付与
  {
    "point_amount": 10,
    "point_amount_unit": "percent",
    "product_code": "978-4-01-%", // 旺文社
  }
]
```

---
`minimum_number_for_combination_purchase`  
```json
{
  "type": "integer",
  "minimum": 1
}
```
複数種別の商品を同時購入したとき、同時購入キャンペーンの対象となる商品種別数の下限です。デフォルトでは未指定で、指定する場合は1以上の整数を指定します。

このパラメータを指定するときは product_based_point_rules で商品毎のルールが指定されている必要があります。
例えば、A商品とB商品とC商品のうち、キャンペーンの発火のために2商品以上が同時購入される必要があるときは 2 を指定します。

例1: 商品A, Bが同時購入されたときに固定ポイント額(200ポイント)付与
```javascript
{
  minimum_number_for_combination_purchase: 2,
  product_based_point_rules: [
    {
      "point_amount": 100,
      "point_amount_unit": "absolute",
      "product_code": "商品Aの商品コード"
    },
    {
      "point_amount": 100,
      "point_amount_unit": "absolute",
      "product_code": "商品Bの商品コード"
    }
  ]
}
```

例2: 商品A, Bが3個ずつ以上同時購入されたときに固定ポイント額(200ポイント)付与
```javascript
{
  minimum_number_for_combination_purchase: 2,
  product_based_point_rules: [
    {
      "point_amount": 100,
      "point_amount_unit": "absolute",
      "product_code": "商品Aの商品コード",
      "required_count": 3
    },
    {
      "point_amount": 100,
      "point_amount_unit": "absolute",
      "product_code": "商品Bの商品コード",
      "required_count": 3
    }
  ]
}
```

例2: 商品A, B, Cのうち2商品以上が同時購入されたときに総額の10%ポイントが付与
```javascript
{
  minimum_number_for_combination_purchase: 2,
  product_based_point_rules: [
    {
      "point_amount": 10,
      "point_amount_unit": "percent",
      "product_code": "商品Aの商品コード",
      "is_multiply_by_count": true,
    },
    {
      "point_amount": 10,
      "point_amount_unit": "percent",
      "product_code": "商品Bの商品コード",
      "is_multiply_by_count": true,
    },
    {
      "point_amount": 10,
      "point_amount_unit": "percent",
      "product_code": "商品Cの商品コード",
      "is_multiply_by_count": true,
    }
  ]
}
```

---
`exist_in_each_product_groups`  
```json
{
  "type": "boolean"
}
```
複数の商品グループの各グループにつき1種類以上の商品が購入されることによって発火するキャンペーンであるときに真を指定します。デフォルトは偽です。

このパラメータを指定するときは product_based_point_rules で商品毎のルールが指定され、さらにその中でgroup_idが指定されている必要があります。group_idは正の整数です。
exist_in_each_product_groupsが指定されているにも関わらず商品毎のルールでgroup_idが指定されていないものが含まれている場合はinvalid_parametersエラー(missing group_id, エラーコード400)が返ります。

例えば、商品グループA(商品コードa1, a2)、商品グループB(商品コードb1, b2)の2つの商品グループがあるとします。
このとき、各商品グループからそれぞれ少なくとも1種類以上の商品が購入されることにより発火するキャンペーンに対するリクエストパラメータは以下のようなものになります。

```javascript
{
  exist_in_each_product_groups: true,
  product_based_point_rules: [
    {
      "point_amount": 100,
      "point_amount_unit": "absolute",
      "product_code": "a1",
      "group_id": 1
    },
    {
      "point_amount": 100,
      "point_amount_unit": "absolute",
      "product_code": "a2",
      "group_id": 1
    },
    {
      "point_amount": 200,
      "point_amount_unit": "absolute",
      "product_code": "b1",
      "group_id": 2
    },
    {
      "point_amount": 200,
      "point_amount_unit": "absolute",
      "product_code": "b2",
      "group_id": 2
    }
  ]
}
```

このキャンペーンが設定された状態で、商品a1、b1が同時に購入された場合、各商品に対する個別のルールが適用された上での総和がポイント付与値になります。つまり100 + 200=300がポイント付与値になります。商品a1、a2、 b1、b2が同時に購入された場合は100 + 100 + 200 + 200=600がポイント付与値になります。 商品a1、a2が同時に購入された場合は全商品グループから1種以上購入されるという条件を満たしていないためポイントは付与されません。

ポイント付与値を各商品毎のルールの総和ではなく固定値にしたい場合には、max_point_amountを指定します。
例えば以下のようなリクエストパラメータ指定の場合を考えます。

```javascript
{
  max_point_amount: 100,
  exist_in_each_product_groups: true,
  product_based_point_rules: [
    {
      "point_amount": 100,
      "point_amount_unit": "absolute",
      "product_code": "a1",
      "group_id": 1
    },
    {
      "point_amount": 100,
      "point_amount_unit": "absolute",
      "product_code": "a2",
      "group_id": 1
    },
    {
      "point_amount": 100,
      "point_amount_unit": "absolute",
      "product_code": "b1",
      "group_id": 2
    },
    {
      "point_amount": 100,
      "point_amount_unit": "absolute",
      "product_code": "b2",
      "group_id": 2
    }
  ]
}
```

このキャンペーンが設定された状態で、商品a1、b1が同時に購入された場合、各商品に対する個別のルールが適用された上での総和がポイント付与値になりますが、付与値の上限が100ポイントになります。つまり100 + 200=300と計算されますが上限額の100ポイントが実際の付与値になります。商品a1、a2、 b1、b2が同時に購入された場合は100 + 100 + 200 + 200=600ですが上限額の100がポイント付与値になります。 商品a1、a2が同時に購入された場合は全商品グループから1種以上購入されるという条件を満たしていないためポイントは付与されません。

---
`max_point_amount`  
```json
{
  "type": "integer",
  "minimum": 1
}
```
キャンペーンによって付与されるポイントの上限を指定します。デフォルトは未指定です。

このパラメータが指定されている場合、amount_based_point_rules や product_based_point_rules によって計算されるポイント付与値がmax_point_amountを越えている場合、max_point_amountの値がポイント付与値となり、越えていない場合はその値がポイント付与値となります。

---
`max_total_point_amount`  
```json
{
  "type": "integer",
  "minimum": 1
}
```
キャンペーンによって付与される1人当たりの累計ポイント数の上限を指定します。デフォルトは未指定です。

このパラメータが指定されている場合、各ユーザに対してそのキャンペーンによって過去付与されたポイントの累積値が記録されるようになります。
累積ポイント数がmax_total_point_amountを超えない限りにおいてキャンペーンで算出されたポイントが付与されます。

---
`dest_private_money_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
キャンペーンを駆動するイベントのマネーとは「別のマネー」に対してポイントを付けたいときに、そのマネーIDを指定します。

ポイント付与先のマネーはキャンペーンを駆動するイベントのマネーと同一発行体が発行しているものに限ります。その他のマネーIDが指定された場合は private_money_not_found (422) が返ります。
エンドユーザー、店舗、ポイント負担先店舗はポイント付与先マネーのウォレットを持っている必要があります。持っていない場合はポイントは付きません。
元のイベントのマネーと異なる複数のマネーに対して同時にポイントを付与することはできません。重複可能に設定されている複数のキャンペーンで別々のポイント付与先マネーを指定した場合は最も優先度の高いものが処理され、残りは無視されます。
キャンペーンのポイント付与先マネーは後から更新することはできません。
デフォルトではポイント付与先はキャンペーンを駆動するイベントのマネー(private_money_idで指定したマネー)になります。

別マネーに対するポイント付与は別のtransactionとなります。 RefundTransaction で元のイベントをキャンセルしたときはポイント付与のtransactionもキャンセルされ、逆にポイント付与のtransactionをキャンセルしたときは連動して元のイベントがキャンセルされます。

---
`applicable_account_metadata`  
```json
{
  "type": "object"
}
```
ウォレットに紐付くメタデータが特定の値を持つときにのみ発火するキャンペーンを登録します。
メタデータの属性名 key とメタデータの値 value の組をオブジェクトとして指定します。
ウォレットのメタデータはCreateUserAccountやUpdateCustomerAccountで登録できます。

オプショナルパラメータtestによって比較方法を指定することができます。
デフォルトは equal で、その他に not-equalを指定可能です。

例1: 取引が行なわれたウォレットのメタデータに住所として東京が指定されているときのみ発火

```javascript
{
  "key": "prefecture",
  "value": "tokyo"
}
```

例2: 取引が行なわれたウォレットのメタデータに住所として東京以外が指定されているときのみ発火

```javascript
{
  "key": "prefecture",
  "value": "tokyo",
  "test": "not-equal"
}
```

---
`budget_caps_amount`  
```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 10000000000
}
```
キャンペーンの予算上限を指定します。デフォルトは未指定です。

このパラメータが指定されている場合、このキャンペーンの適用により付与されたポイント全体を定期的に集計し、その合計が上限を越えていた場合にはキャンペーンを無効にします。
一度この値を越えて無効となったキャンペーンを再度有効にすることは出来ません。

---
成功したときは[Campaign](#campaign)オブジェクトを返します
<a name="list-campaigns"></a>
#### キャンペーン一覧を取得する
マネーIDを指定してキャンペーンを取得します。
発行体の組織マネージャ権限で、自組織が発行するマネーのキャンペーンについてのみ閲覧可能です。
閲覧権限がない場合は unpermitted_admin_user エラー(422)が返ります。
```typescript
const response: Response<PaginatedCampaigns> = await client.send(new ListCampaigns({
  private_money_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // マネーID
  is_ongoing: false, // 現在適用可能なキャンペーンかどうか
  available_from: "2022-01-01T10:00:15.000000Z", // 指定された日時以降に適用可能期間が含まれているか
  available_to: "2020-05-31T11:36:43.000000Z", // 指定された日時以前に適用可能期間が含まれているか
  page: 1, // ページ番号
  per_page: 20 // 1ページ分の取得数
}));
```

---
`private_money_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
マネーIDです。

フィルターとして使われ、指定したマネーでのキャンペーンのみ一覧に表示されます。

---
`is_ongoing`  
```json
{
  "type": "boolean"
}
```
有効化されており、現在キャンペーン期間内にあるキャンペーンをフィルターするために使われます。
真であれば適用可能なもののみを抽出し、偽であれば適用不可なもののみを抽出します。
デフォルトでは未指定(フィルターなし)です。

---
`available_from`  
```json
{
  "type": "string",
  "format": "date-time"
}
```
キャンペーン終了日時が指定された日時以降であるキャンペーンをフィルターするために使われます。
デフォルトでは未指定(フィルターなし)です。

---
`available_to`  
```json
{
  "type": "string",
  "format": "date-time"
}
```
キャンペーン開始日時が指定された日時以前であるキャンペーンをフィルターするために使われます。
デフォルトでは未指定(フィルターなし)です。

---
`page`  
```json
{
  "type": "integer",
  "minimum": 1
}
```
取得したいページ番号です。

---
`per_page`  
```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 50
}
```
1ページ分の取得数です。デフォルトでは 20 になっています。

---
成功したときは[PaginatedCampaigns](#paginated-campaigns)オブジェクトを返します
<a name="get-campaign"></a>
#### キャンペーンを取得する
IDを指定してキャンペーンを取得します。
発行体の組織マネージャ権限で、自組織が発行するマネーのキャンペーンについてのみ閲覧可能です。
閲覧権限がない場合は unpermitted_admin_user エラー(422)が返ります。
```typescript
const response: Response<Campaign> = await client.send(new GetCampaign({
  campaign_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" // キャンペーンID
}));
```

---
`campaign_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
キャンペーンIDです。

指定したIDのキャンペーンを取得します。存在しないIDを指定した場合は404エラー(NotFound)が返ります。

---
成功したときは[Campaign](#campaign)オブジェクトを返します
<a name="update-campaign"></a>
#### ポイント付与キャンペーンを更新する
ポイント付与キャンペーンを更新します。

```typescript
const response: Response<Campaign> = await client.send(new UpdateCampaign({
  campaign_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // キャンペーンID
  name: "byfcjYNDVx4A2ovqPMZA8irXJ9E6ZcMzkLyAqgwSoddiujWTgn11mpxaVIYgQo5GvBiHKw3I5f57jFE45d3P21Pzx2jnlKrw0LdNS", // キャンペーン名
  starts_at: "2020-05-12T19:19:16.000000Z", // キャンペーン開始日時
  ends_at: "2022-06-26T17:10:33.000000Z", // キャンペーン終了日時
  priority: 8101, // キャンペーンの適用優先度
  event: "topup", // イベント種別
  description: "tkXCDrt0LJOE3QgwrCcszhfH09Y5OthVwPmvHXBFS5mnHJDaN7ByqCBViT8YJSc5gafw5E7JxTvjUc1aT5EbGpCQn8B7l65BYMvNkhEwbRq7C0zj85JoEScisdzkhxnXFFT7CX", // キャンペーンの説明文
  status: "disabled", // キャンペーン作成時の状態
  point_expires_at: "2024-01-25T19:14:44.000000Z", // ポイント有効期限(絶対日時指定)
  point_expires_in_days: 7438, // ポイント有効期限(相対日数指定)
  is_exclusive: false, // キャンペーンの重複設定
  subject: "money", // ポイント付与の対象金額の種別
  amount_based_point_rules: [{
  "point_amount": 5,
  "point_amount_unit": "percent",
  "subject_more_than_or_equal": 1000,
  "subject_less_than": 5000
}], // 取引金額ベースのポイント付与ルール
  product_based_point_rules: [{
  "point_amount": 5,
  "point_amount_unit": "percent",
  "product_code": "4912345678904",
  "is_multiply_by_count": true,
  "required_count": 2
}, {
  "point_amount": 5,
  "point_amount_unit": "percent",
  "product_code": "4912345678904",
  "is_multiply_by_count": true,
  "required_count": 2
}, {
  "point_amount": 5,
  "point_amount_unit": "percent",
  "product_code": "4912345678904",
  "is_multiply_by_count": true,
  "required_count": 2
}], // 商品情報ベースのポイント付与ルール
  applicable_days_of_week: [1, 6], // キャンペーンを適用する曜日 (複数指定)
  applicable_time_ranges: [{
  "from": "12:00",
  "to": "23:59"
}, {
  "from": "12:00",
  "to": "23:59"
}, {
  "from": "12:00",
  "to": "23:59"
}], // キャンペーンを適用する時間帯 (複数指定)
  applicable_shop_ids: ["xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"], // キャンペーン適用対象となる店舗IDのリスト
  minimum_number_for_combination_purchase: 2003, // 複数種類の商品を同時購入するときの商品種別数の下限
  exist_in_each_product_groups: false, // 複数の商品グループにつき1種類以上の商品購入によって発火するキャンペーンの指定フラグ
  max_point_amount: 7120, // キャンペーンによって付与されるポイントの上限
  max_total_point_amount: 30, // キャンペーンによって付与されるの1人当たりの累計ポイントの上限
  applicable_account_metadata: {
  "key": "sex",
  "value": "male"
}, // ウォレットに紐付くメタデータが特定の値を持つときにのみ発火するキャンペーンを登録します。
  budget_caps_amount: 306881955 // キャンペーン予算上限
}));
```

---
`campaign_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
キャンペーンIDです。

指定したIDのキャンペーンを更新します。存在しないIDを指定した場合は404エラー(NotFound)が返ります。

---
`name`  
```json
{
  "type": "string",
  "maxLength": 256
}
```
キャンペーン名です。

ポイント付与によってできるチャージ取引の説明文に転記されます。取引説明文はエンドユーザーからも確認できます。

---
`starts_at`  
```json
{
  "type": "string",
  "format": "date-time"
}
```
キャンペーン開始日時です。
キャンペーン期間中のみポイントが付与されます。
開始日時よりも終了日時が前のときはcampaign_invalid_periodエラー(422)になります。

---
`ends_at`  
```json
{
  "type": "string",
  "format": "date-time"
}
```
キャンペーン終了日時です。
キャンペーン期間中のみポイントが付与されます。
開始日時よりも終了日時が前のときはcampaign_invalid_periodエラー(422)になります。

---
`priority`  
```json
{
  "type": "integer"
}
```
キャンペーンの適用優先度です。

優先度が大きいものから順に適用判定されていきます。
キャンペーン期間が重なっている同一の優先度のキャンペーンが存在するとcampaign_period_overlapsエラー(422)になります。

---
`event`  
```json
{
  "type": "string",
  "enum": [
    "topup",
    "payment",
    "external-transaction"
  ]
}
```
キャンペーンのトリガーとなるイベントの種類を指定します。

以下のいずれかを指定できます。

1. topup
   店舗からエンドユーザーへの送金取引(チャージ)
2. payment
   エンドユーザーから店舗への送金取引(支払い)
3. external-transaction
   ポケペイ外の取引(現金決済など)

---
`description`  
```json
{
  "type": "string",
  "maxLength": 200
}
```
キャンペーンの内容を記載します。管理画面などでキャンペーンを管理するための説明文になります。

---
`status`  
```json
{
  "type": "string",
  "enum": [
    "enabled",
    "disabled"
  ]
}
```
キャンペーン作成時の状態を指定します。デフォルトではenabledです。

以下のいずれかを指定できます。

1. enabled
   有効
2. disabled
   無効

---
`point_expires_at`  
```json
{
  "type": "string",
  "format": "date-time"
}
```
キャンペーンによって付与されるポイントの有効期限を絶対日時で指定します。
省略した場合はマネーに設定された有効期限と同じものがポイントの有効期限となります。

---
`point_expires_in_days`  
```json
{
  "type": "integer",
  "minimum": 1
}
```
キャンペーンによって付与されるポイントの有効期限を相対日数で指定します。
省略した場合はマネーに設定された有効期限と同じものがポイントの有効期限となります。

---
`is_exclusive`  
```json
{
  "type": "boolean"
}
```
キャンペーンの重ね掛けを行うかどうかのフラグです。

これにtrueを指定すると他のキャンペーンと同時適用されません。デフォルト値はtrueです。
falseを指定すると次の優先度の重ね掛け可能なキャンペーンの適用判定に進みます。

---
`subject`  
```json
{
  "type": "string",
  "enum": [
    "money",
    "all"
  ]
}
```
ポイント付与額を計算する対象となる金額の種類を指定します。デフォルト値はallです。
eventとしてexternal-transactionを指定した場合はポイントとマネーの区別がないためsubjectの指定に関わらず常にallとなります。

以下のいずれかを指定できます。

1. money
moneyを指定すると決済額の中で「マネー」を使って支払った額を対象にします

2. all
all を指定すると決済額全体を対象にします (「ポイント」での取引額を含む)
注意: event を topup にしたときはポイントの付与に対しても適用されます

---
`amount_based_point_rules`  
```json
{
  "type": "array",
  "items": {
    "type": "object"
  }
}
```
金額をベースとしてポイント付与を行うルールを指定します。
amount_based_point_rules と product_based_point_rules はどちらか一方しか指定できません。
各ルールは一つのみ適用され、条件に重複があった場合は先に記載されたものが優先されます。

例:
```javascript
[
  // 1000円以上、5000円未満の決済には 5％
  {
    "point_amount": 5,
    "point_amount_unit": "percent",
    "subject_more_than_or_equal": 1000,
    "subject_less_than": 5000
  },
  // 5000円以上の決済には 10%
  {
    "point_amount": 10,
    "point_amount_unit": "percent",
    "subject_more_than_or_equal": 5000
  },
]
```

---
`product_based_point_rules`  
```json
{
  "type": "array",
  "items": {
    "type": "object"
  }
}
```
商品情報をベースとしてポイント付与を行うルールを指定します。
ルールは商品ごとに設定可能で、ルールの配列として指定します。
amount_based_point_rules と product_based_point_rules はどちらか一方しか指定できません。
event が payment か external-transaction の時のみ有効です。
各ルールの順序は問わず、適用可能なものは全て適用されます。
一つの決済の中で複数の商品がキャンペーン適用可能な場合はそれぞれの商品についてのルールが適用され、ポイント付与額はその合算になります。

例:
```javascript
[
  // 対象商品の購入額から5%ポイント付与。複数購入時は単価の5%が付与される。
  {
    "point_amount": 5,
    "point_amount_unit": "percent",
    "product_code": "4912345678904",
  },
  // 対象商品の購入額から5%ポイント付与。複数購入時は購入総額の5%が付与される。
  {
    "point_amount": 5,
    "point_amount_unit": "percent",
    "product_code": "4912345678904",
    "is_multiply_by_count": true,
  },
  // 対象商品を2つ以上購入したら500ポイント付与(固定額付与)
  {
    "point_amount": 500,
    "point_amount_unit": "absolute",
    "product_code": "4912345678904",
    "required_count": 2
  },
  // 書籍は10%ポイント付与
  // ※ISBNの形式はレジがポケペイに送信する形式に準じます
  {
    "point_amount": 10,
    "point_amount_unit": "percent",
    "product_code": "978-%",
  },
  // 一部の出版社の書籍は10%ポイント付与
  {
    "point_amount": 10,
    "point_amount_unit": "percent",
    "product_code": "978-4-01-%", // 旺文社
  }
]
```

---
`minimum_number_for_combination_purchase`  
```json
{
  "type": "integer",
  "minimum": 1
}
```
複数種別の商品を同時購入したとき、同時購入キャンペーンの対象となる商品種別数の下限です。

このパラメータを指定するときは product_based_point_rules で商品毎のルールが指定されている必要があります。
例えば、A商品とB商品とC商品のうち、キャンペーンの発火のために2商品以上が同時購入される必要があるときは 2 を指定します。

例1: 商品A, Bが同時購入されたときに固定ポイント額(200ポイント)付与
```javascript
{
  minimum_number_for_combination_purchase: 2,
  product_based_point_rules: [
    {
      "point_amount": 100,
      "point_amount_unit": "absolute",
      "product_code": "商品Aの商品コード"
    },
    {
      "point_amount": 100,
      "point_amount_unit": "absolute",
      "product_code": "商品Bの商品コード"
    }
  ]
}
```

例2: 商品A, Bが3個ずつ以上同時購入されたときに固定ポイント額(200ポイント)付与
```javascript
{
  minimum_number_for_combination_purchase: 2,
  product_based_point_rules: [
    {
      "point_amount": 100,
      "point_amount_unit": "absolute",
      "product_code": "商品Aの商品コード",
      "required_count": 3
    },
    {
      "point_amount": 100,
      "point_amount_unit": "absolute",
      "product_code": "商品Bの商品コード",
      "required_count": 3
    }
  ]
}
```

例2: 商品A, B, Cのうち2商品以上が同時購入されたときに総額の10%ポイントが付与
```javascript
{
  minimum_number_for_combination_purchase: 2,
  product_based_point_rules: [
    {
      "point_amount": 10,
      "point_amount_unit": "percent",
      "product_code": "商品Aの商品コード",
      "is_multiply_by_count": true,
    },
    {
      "point_amount": 10,
      "point_amount_unit": "percent",
      "product_code": "商品Bの商品コード",
      "is_multiply_by_count": true,
    },
    {
      "point_amount": 10,
      "point_amount_unit": "percent",
      "product_code": "商品Cの商品コード",
      "is_multiply_by_count": true,
    }
  ]
}
```

---
`exist_in_each_product_groups`  
```json
{
  "type": "boolean"
}
```
複数の商品グループの各グループにつき1種類以上の商品が購入されることによって発火するキャンペーンであるときに真を指定します。デフォルトは偽です。

このパラメータを指定するときは product_based_point_rules で商品毎のルールが指定され、さらにその中でgroup_idが指定されている必要があります。group_idは正の整数です。
exist_in_each_product_groupsが指定されているにも関わらず商品毎のルールでgroup_idが指定されていないものが含まれている場合はinvalid_parametersエラー(missing group_id, エラーコード400)が返ります。

例えば、商品グループA(商品コードa1, a2)、商品グループB(商品コードb1, b2)の2つの商品グループがあるとします。
このとき、各商品グループからそれぞれ少なくとも1種類以上の商品が購入されることにより発火するキャンペーンに対するリクエストパラメータは以下のようなものになります。

```javascript
{
  exist_in_each_product_groups: true,
  product_based_point_rules: [
    {
      "point_amount": 100,
      "point_amount_unit": "absolute",
      "product_code": "a1",
      "group_id": 1
    },
    {
      "point_amount": 100,
      "point_amount_unit": "absolute",
      "product_code": "a2",
      "group_id": 1
    },
    {
      "point_amount": 200,
      "point_amount_unit": "absolute",
      "product_code": "b1",
      "group_id": 2
    },
    {
      "point_amount": 200,
      "point_amount_unit": "absolute",
      "product_code": "b2",
      "group_id": 2
    }
  ]
}
```

このキャンペーンが設定された状態で、商品a1、b1が同時に購入された場合、各商品に対する個別のルールが適用された上での総和がポイント付与値になります。つまり100 + 200=300がポイント付与値になります。商品a1、a2、 b1、b2が同時に購入された場合は100 + 100 + 200 + 200=600がポイント付与値になります。 商品a1、a2が同時に購入された場合は全商品グループから1種以上購入されるという条件を満たしていないためポイントは付与されません。

ポイント付与値を各商品毎のルールの総和ではなく固定値にしたい場合には、max_point_amountを指定します。
例えば以下のようなリクエストパラメータ指定の場合を考えます。

```javascript
{
  max_point_amount: 100,
  exist_in_each_product_groups: true,
  product_based_point_rules: [
    {
      "point_amount": 100,
      "point_amount_unit": "absolute",
      "product_code": "a1",
      "group_id": 1
    },
    {
      "point_amount": 100,
      "point_amount_unit": "absolute",
      "product_code": "a2",
      "group_id": 1
    },
    {
      "point_amount": 100,
      "point_amount_unit": "absolute",
      "product_code": "b1",
      "group_id": 2
    },
    {
      "point_amount": 100,
      "point_amount_unit": "absolute",
      "product_code": "b2",
      "group_id": 2
    }
  ]
}
```

このキャンペーンが設定された状態で、商品a1、b1が同時に購入された場合、各商品に対する個別のルールが適用された上での総和がポイント付与値になりますが、付与値の上限が100ポイントになります。つまり100 + 200=300と計算されますが上限額の100ポイントが実際の付与値になります。商品a1、a2、 b1、b2が同時に購入された場合は100 + 100 + 200 + 200=600ですが上限額の100がポイント付与値になります。 商品a1、a2が同時に購入された場合は全商品グループから1種以上購入されるという条件を満たしていないためポイントは付与されません。

---
`max_point_amount`  
```json
{
  "type": "integer",
  "minimum": 1
}
```
キャンペーンによって付与される1取引当たりのポイント数の上限を指定します。デフォルトは未指定です。

このパラメータが指定されている場合、amount_based_point_rules や product_based_point_rules によって計算されるポイント付与値がmax_point_amountを越えている場合、max_point_amountの値がポイント付与値となり、越えていない場合はその値がポイント付与値となります。

---
`max_total_point_amount`  
```json
{
  "type": "integer",
  "minimum": 1
}
```
キャンペーンによって付与される1人当たりの累計ポイント数の上限を指定します。デフォルトは未指定です。

このパラメータが指定されている場合、各ユーザに対してそのキャンペーンによって過去付与されたポイントの累積値が記録されるようになります。
累積ポイント数がmax_total_point_amountを超えない限りにおいてキャンペーンで算出されたポイントが付与されます。

---
`applicable_account_metadata`  
```json
{
  "type": "object"
}
```
ウォレットに紐付くメタデータが特定の値を持つときにのみ発火するキャンペーンを登録します。
メタデータの属性名 key とメタデータの値 value の組をオブジェクトとして指定します。
ウォレットのメタデータはCreateUserAccountやUpdateCustomerAccountで登録できます。

オプショナルパラメータtestによって比較方法を指定することができます。
デフォルトは equal で、その他に not-equalを指定可能です。

例1: 取引が行なわれたウォレットのメタデータに住所として東京が指定されているときのみ発火

```javascript
{
  "key": "prefecture",
  "value": "tokyo"
}
```

例2: 取引が行なわれたウォレットのメタデータに住所として東京以外が指定されているときのみ発火

```javascript
{
  "key": "prefecture",
  "value": "tokyo",
  "test": "not-equal"
}
```

---
`budget_caps_amount`  
```json
{
  "type": "integer",
  "minimum": 1,
  "maximum": 10000000000
}
```
キャンペーンの予算上限を指定します。

キャンペーン予算上限が設定されておらずこのパラメータに数値が指定されている場合、このキャンペーンの適用により付与されたポイント全体を定期的に集計し、その合計が上限を越えていた場合にはキャンペーンを無効にします。
一度この値を越えて無効となったキャンペーンを再度有効にすることは出来ません。
キャンペーン予算上限が設定されておらずこのパラメータにnullが指定されている場合、何も発生しない。
キャンペーン予算上限が設定されておりこのパラメータにnullが指定された場合、キャンペーン予算上限は止まります。

---
成功したときは[Campaign](#campaign)オブジェクトを返します
### Webhook
Webhookは特定のワーカータスクでの処理が完了した事を通知します。
WebHookにはURLとタスク名、有効化されているかを設定することが出来ます。
通知はタスク完了時、事前に設定したURLにPOSTリクエストを行います。

<a name="create-webhook"></a>
#### webhookの作成
ワーカータスクの処理が終了したことを通知するためのWebhookを登録します
このAPIにより指定したタスクの終了時に、指定したURLにPOSTリクエストを送信します。
このとき、リクエストボディは `{"task": <タスク名>}` という値になります。
```typescript
const response: Response<OrganizationWorkerTaskWebhook> = await client.send(new CreateWebhook({
  task: "process_user_stats_operation", // タスク名
  url: "PFa" // URL
}));
```

---
`task`  
```json
{
  "type": "string",
  "enum": [
    "bulk_shops",
    "process_user_stats_operation"
  ]
}
```
ワーカータスク名を指定します

---
`url`  
```json
{
  "type": "string"
}
```
通知先のURLを指定します

---
成功したときは[OrganizationWorkerTaskWebhook](#organization-worker-task-webhook)オブジェクトを返します
<a name="list-webhooks"></a>
#### 作成したWebhookの一覧を返す
```typescript
const response: Response<PaginatedOrganizationWorkerTaskWebhook> = await client.send(new ListWebhooks({
  page: 1, // ページ番号
  per_page: 50 // 1ページ分の取得数
}));
```

---
`page`  
```json
{
  "type": "integer",
  "minimum": 1
}
```
取得したいページ番号です。

---
`per_page`  
```json
{
  "type": "integer",
  "minimum": 1
}
```
1ページ分の取得数です。デフォルトでは 50 になっています。

---
成功したときは[PaginatedOrganizationWorkerTaskWebhook](#paginated-organization-worker-task-webhook)オブジェクトを返します
<a name="update-webhook"></a>
#### Webhookの更新
指定したWebhookの内容を更新します
```typescript
const response: Response<OrganizationWorkerTaskWebhook> = await client.send(new UpdateWebhook({
  webhook_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // Webhook ID
  url: "2Q0QZF", // URL
  is_active: true, // 有効/無効
  task: "bulk_shops" // タスク名
}));
```

---
`webhook_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
更新するWebhookのIDです。

---
`url`  
```json
{
  "type": "string"
}
```
変更するURLを指定します

---
`is_active`  
```json
{
  "type": "boolean"
}
```
trueならWebhookによる通知が有効になり、falseなら無効になります

---
`task`  
```json
{
  "type": "string",
  "enum": [
    "bulk_shops",
    "process_user_stats_operation"
  ]
}
```
指定したタスクが終了したときにWebhookによる通知がされます

---
成功したときは[OrganizationWorkerTaskWebhook](#organization-worker-task-webhook)オブジェクトを返します
<a name="delete-webhook"></a>
#### Webhookの削除
指定したWebhookを削除します
```typescript
const response: Response<OrganizationWorkerTaskWebhook> = await client.send(new DeleteWebhook({
  webhook_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" // Webhook ID
}));
```

---
`webhook_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
削除するWebhookのIDです。

---
成功したときは[OrganizationWorkerTaskWebhook](#organization-worker-task-webhook)オブジェクトを返します
### Coupon
Couponは支払い時に指定し、支払い処理の前にCouponに指定の方法で値引き処理を行います。
Couponは特定店舗で利用できるものや利用可能期間、配信条件などを設定できます。

<a name="list-coupons"></a>
#### クーポン一覧の取得
指定したマネーのクーポン一覧を取得します
```typescript
const response: Response<PaginatedCoupons> = await client.send(new ListCoupons({
  private_money_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // 対象クーポンのマネーID
  coupon_id: "PWcwwu3uh", // クーポンID
  coupon_name: "9f", // クーポン名
  issued_shop_name: "L3S3N", // 発行店舗名
  available_shop_name: "vBIxMXxVO", // 利用可能店舗名
  available_from: "2020-12-04T01:56:35.000000Z", // 利用可能期間 (開始日時)
  available_to: "2022-10-18T15:11:52.000000Z", // 利用可能期間 (終了日時)
  page: 1, // ページ番号
  per_page: 50 // 1ページ分の取得数
}));
```

---
`private_money_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
対象クーポンのマネーIDです(必須項目)。
存在しないマネーIDを指定した場合はprivate_money_not_foundエラー(422)が返ります。


---
`coupon_id`  
```json
{
  "type": "string"
}
```
指定されたクーポンIDで結果をフィルターします。
部分一致(前方一致)します。


---
`coupon_name`  
```json
{
  "type": "string"
}
```
指定されたクーポン名で結果をフィルターします。


---
`issued_shop_name`  
```json
{
  "type": "string"
}
```
指定された発行店舗で結果をフィルターします。


---
`available_shop_name`  
```json
{
  "type": "string"
}
```
指定された利用可能店舗で結果をフィルターします。


---
`available_from`  
```json
{
  "type": "string",
  "format": "date-time"
}
```
利用可能期間でフィルターします。フィルターの開始日時をISO8601形式で指定します。


---
`available_to`  
```json
{
  "type": "string",
  "format": "date-time"
}
```
利用可能期間でフィルターします。フィルターの終了日時をISO8601形式で指定します。


---
`page`  
```json
{
  "type": "integer",
  "minimum": 1
}
```
取得したいページ番号です。

---
`per_page`  
```json
{
  "type": "integer",
  "minimum": 1
}
```
1ページ分の取得数です。デフォルトでは 50 になっています。

---
成功したときは[PaginatedCoupons](#paginated-coupons)オブジェクトを返します
<a name="create-coupon"></a>
#### クーポンの登録
新しいクーポンを登録します
```typescript
const response: Response<CouponDetail> = await client.send(new CreateCoupon({
  private_money_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx",
  name: "VOpiS1EeKe2EnvF9kW30yXFj5pEZQNOtIwcrR2Tap7tnXzfq7vVXcZZXkAjYTEO65NQtFJaRQvj5yyqZjpM3EGDvxc2vHpfKAF",
  starts_at: "2023-12-27T02:00:10.000000Z",
  ends_at: "2020-12-24T15:11:19.000000Z",
  issued_shop_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // 発行元の店舗ID
  description: "MK87o5EDfCnjGchqfzXJGnbGhZsKdVrETxLEt4GFvxAKZGN2hkrp4AuDVFN5fAvBVJFsjezB3YP3w02SjMN6p0E72qWtOk3QUVbESEWPtcFyu37VMAkI2ylOPtFPfUfw5cNQlmY98v9Ekah2FpsKs0KWXhqcS1Ua3AE",
  discount_amount: 7493,
  discount_percentage: 1817.0,
  discount_upper_limit: 6246,
  display_starts_at: "2023-12-14T13:09:00.000000Z", // クーポンの掲載期間(開始日時)
  display_ends_at: "2020-10-11T12:17:29.000000Z", // クーポンの掲載期間(終了日時)
  is_disabled: true, // 無効化フラグ
  is_hidden: false, // クーポン一覧に掲載されるかどうか
  is_public: false, // アプリ配信なしで受け取れるかどうか
  code: "Coy2", // クーポン受け取りコード
  usage_limit: 2811, // ユーザごとの利用可能回数(NULLの場合は無制限)
  min_amount: 8036, // クーポン適用可能な最小取引額
  is_shop_specified: false, // 特定店舗限定のクーポンかどうか
  available_shop_ids: ["xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"], // 利用可能店舗リスト
  storage_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" // ストレージID
}));
```
`is_shop_specified`と`available_shop_ids`は同時に指定する必要があります。


---
`is_hidden`  
```json
{
  "type": "boolean"
}
```
アプリに表示されるクーポン一覧に掲載されるかどうか。
主に一時的に掲載から外したいときに用いられる。そのためis_publicの設定よりも優先される。


---
`storage_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
Storage APIでアップロードしたクーポン画像のStorage IDを指定します

---
成功したときは[CouponDetail](#coupon-detail)オブジェクトを返します
<a name="get-coupon"></a>
#### クーポンの取得
指定したIDを持つクーポンを取得します
```typescript
const response: Response<CouponDetail> = await client.send(new GetCoupon({
  coupon_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" // クーポンID
}));
```

---
`coupon_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
取得するクーポンのIDです。
UUIDv4フォーマットである必要があり、フォーマットが異なる場合は InvalidParametersエラー(400)が返ります。
指定したIDのクーポンが存在しない場合はCouponNotFoundエラー(422)が返ります。

---
成功したときは[CouponDetail](#coupon-detail)オブジェクトを返します
<a name="update-coupon"></a>
#### クーポンの更新
指定したクーポンを更新します
```typescript
const response: Response<CouponDetail> = await client.send(new UpdateCoupon({
  coupon_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // クーポンID
  name: "tWk5Skp4k9FjiQcyxviUOicaOZqLE3MkcTFrJK4NHPvl4VhqOdqyKHcIOPhbvogj2mEAT9kQkxX80ARofdpsoiXVeBxFuF7c05YcbHgR",
  description: "SFdYgsuZbSsGmFYxkuLrQMChiww3RYCIbC9pf8Wzgm4choir96Zk4wBbHbRE9tWUhNPatHCNYgstx4oloda7k12vM37GlbZJKSAFS4eQAmyXqltVLiYXrByWE1iViSMuTkME7Xo3gZLzoJUOW0EXfGSkB9sMClBaFjZtZBNIprWMfHv0Adc0",
  discount_amount: 9517,
  discount_percentage: 7738.0,
  discount_upper_limit: 2558,
  starts_at: "2020-06-21T15:37:39.000000Z",
  ends_at: "2021-11-26T03:58:42.000000Z",
  display_starts_at: "2022-11-02T16:38:43.000000Z", // クーポンの掲載期間(開始日時)
  display_ends_at: "2023-02-18T02:15:15.000000Z", // クーポンの掲載期間(終了日時)
  is_disabled: false, // 無効化フラグ
  is_hidden: false, // クーポン一覧に掲載されるかどうか
  is_public: false, // アプリ配信なしで受け取れるかどうか
  code: "JKZKHW", // クーポン受け取りコード
  usage_limit: 4047, // ユーザごとの利用可能回数(NULLの場合は無制限)
  min_amount: 7303, // クーポン適用可能な最小取引額
  is_shop_specified: false, // 特定店舗限定のクーポンかどうか
  available_shop_ids: ["xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"], // 利用可能店舗リスト
  storage_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" // ストレージID
}));
```
`discount_amount`と`discount_percentage`の少なくとも一方は指定する必要があります。


---
`is_hidden`  
```json
{
  "type": "boolean"
}
```
アプリに表示されるクーポン一覧に掲載されるかどうか。
主に一時的に掲載から外したいときに用いられる。そのためis_publicの設定よりも優先される。


---
`storage_id`  
```json
{
  "type": "string",
  "format": "uuid"
}
```
Storage APIでアップロードしたクーポン画像のStorage IDを指定します

---
成功したときは[CouponDetail](#coupon-detail)オブジェクトを返します
### UserDevice
UserDeviceはユーザー毎のデバイスを管理します。
あるユーザーが使っている端末を区別する必要がある場合に用いられます。
これが必要な理由はBank Payを用いたチャージを行う場合は端末を区別できることが要件としてあるためです。

<a name="create-user-device"></a>
#### ユーザーのデバイス登録
ユーザーのデバイスを新規に登録します
```typescript
const response: Response<UserDevice> = await client.send(new CreateUserDevice({
  user_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // ユーザーID
  metadata: "{\"user_agent\": \"Mozilla/5.0 (X11; Ubuntu; Linux x86_64; rv:120.0) Gecko/20100101 Firefox/120.0\"}" // ユーザーデバイスのメタデータ
}));
```

---
`metadata`  
```json
{
  "type": "string",
  "format": "json"
}
```
ユーザーのデバイス用の情報をメタデータを保持するために用います。
例: 端末の固有情報やブラウザのUser-Agent


---
成功したときは[UserDevice](#user-device)オブジェクトを返します
<a name="get-user-device"></a>
#### ユーザーのデバイスを取得
ユーザーのデバイスの情報を取得します
```typescript
const response: Response<UserDevice> = await client.send(new GetUserDevice({
  user_device_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" // ユーザーデバイスID
}));
```
成功したときは[UserDevice](#user-device)オブジェクトを返します
<a name="activate-user-device"></a>
#### デバイスの有効化
指定のデバイスを有効化し、それ以外の同一ユーザーのデバイスを無効化します。

```typescript
const response: Response<UserDevice> = await client.send(new ActivateUserDevice({
  user_device_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" // ユーザーデバイスID
}));
```
成功したときは[UserDevice](#user-device)オブジェクトを返します
### BankPay
BankPayを用いた銀行からのチャージ取引などのAPIを提供しています。

<a name="create-bank"></a>
#### 銀行口座の登録
銀行口座の登録を始めるAPIです。レスポンスに含まれるredirect_urlをユーザーの端末で開き銀行を登録します。

ユーザーが銀行口座の登録に成功すると、callback_urlにリクエストが行われます。
アプリの場合はDeep Linkを使うことを想定しています。

```typescript
const response: Response<BankRegisteringInfo> = await client.send(new CreateBank({
  user_device_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // デバイスID
  private_money_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // マネーID
  callback_url: "<Deep Link>", // コールバックURL
  kana: "ポケペイタロウ", // ユーザーの氏名 (片仮名で指定)
  email: "y8Xa1naLbp@7yoC.com", // ユーザーのメールアドレス
  birthdate: "19901142" // 生年月日
}));
```
成功したときは[BankRegisteringInfo](#bank-registering-info)オブジェクトを返します
<a name="list-banks"></a>
#### 登録した銀行の一覧
登録した銀行を一覧します
```typescript
const response: Response<Banks> = await client.send(new ListBanks({
  user_device_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // デバイスID
  private_money_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx"
}));
```
成功したときは[Banks](#banks)オブジェクトを返します
<a name="create-bank-topup-transaction"></a>
#### 銀行からのチャージ
指定のマネーのアカウントにbank_idの口座を用いてチャージを行います。
```typescript
const response: Response<TransactionDetail> = await client.send(new CreateBankTopupTransaction({
  user_device_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // デバイスID
  private_money_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // マネーID
  amount: 3436, // チャージ金額
  bank_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx", // 銀行ID
  request_id: "xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx" // リクエストID
}));
```
成功したときは[TransactionDetail](#transaction-detail)オブジェクトを返します
## Responses


<a name="account-with-user"></a>
## AccountWithUser
* `id (string)`: 
* `name (string)`: 
* `is_suspended (boolean)`: 
* `status (string)`: 
* `private_money (PrivateMoney)`: 
* `user (User)`: 

`private_money`は [PrivateMoney](#private-money) オブジェクトを返します。

`user`は [User](#user) オブジェクトを返します。

<a name="account-detail"></a>
## AccountDetail
* `id (string)`: 
* `name (string)`: 
* `is_suspended (boolean)`: 
* `status (string)`: 
* `balance (number)`: 
* `money_balance (number)`: 
* `point_balance (number)`: 
* `point_debt (number)`: 
* `private_money (PrivateMoney)`: 
* `user (User)`: 
* `external_id (string)`: 

`private_money`は [PrivateMoney](#private-money) オブジェクトを返します。

`user`は [User](#user) オブジェクトを返します。

<a name="account-deleted"></a>
## AccountDeleted

<a name="bill"></a>
## Bill
* `id (string)`: 支払いQRコードのID
* `amount (number)`: 支払い額
* `max_amount (number)`: 支払い額を範囲指定した場合の上限
* `min_amount (number)`: 支払い額を範囲指定した場合の下限
* `description (string)`: 支払いQRコードの説明文(アプリ上で取引の説明文として表示される)
* `account (AccountWithUser)`: 支払いQRコード発行ウォレット
* `is_disabled (boolean)`: 無効化されているかどうか
* `token (string)`: 支払いQRコードを解析したときに出てくるURL

`account`は [AccountWithUser](#account-with-user) オブジェクトを返します。

<a name="check"></a>
## Check
* `id (string)`: チャージQRコードのID
* `created_at (string)`: チャージQRコードの作成日時
* `amount (number)`: チャージマネー額 (deprecated)
* `money_amount (number)`: チャージマネー額
* `point_amount (number)`: チャージポイント額
* `description (string)`: チャージQRコードの説明文(アプリ上で取引の説明文として表示される)
* `user (User)`: 送金元ユーザ情報
* `is_onetime (boolean)`: 使用回数が一回限りかどうか
* `is_disabled (boolean)`: 無効化されているかどうか
* `expires_at (string)`: チャージQRコード自体の失効日時
* `last_used_at (string)`: 
* `private_money (PrivateMoney)`: 対象マネー情報
* `usage_limit (number)`: 一回限りでない場合の最大読み取り回数
* `usage_count (number)`: 一回限りでない場合の現在までに読み取られた回数
* `point_expires_at (string)`: ポイント有効期限(絶対日数指定)
* `point_expires_in_days (number)`: ポイント有効期限(相対日数指定)
* `token (string)`: チャージQRコードを解析したときに出てくるURL

`user`は [User](#user) オブジェクトを返します。

`private_money`は [PrivateMoney](#private-money) オブジェクトを返します。

<a name="paginated-checks"></a>
## PaginatedChecks
* `rows (Check[])`: 
* `count (number)`: 
* `pagination (Pagination)`: 

`rows`は [Check](#check) オブジェクトの配列を返します。

`pagination`は [Pagination](#pagination) オブジェクトを返します。

<a name="cpm-token"></a>
## CpmToken
* `cpm_token (string)`: 
* `account (AccountDetail)`: 
* `transaction (Transaction)`: 
* `event (ExternalTransaction)`: 
* `scopes (string[])`: 許可された取引種別
* `expires_at (string)`: CPMトークンの失効日時
* `metadata (string)`: エンドユーザー側メタデータ

`account`は [AccountDetail](#account-detail) オブジェクトを返します。

`transaction`は [Transaction](#transaction) オブジェクトを返します。

`event`は [ExternalTransaction](#external-transaction) オブジェクトを返します。

<a name="cashtray"></a>
## Cashtray
* `id (string)`: Cashtray自体のIDです。
* `amount (number)`: 取引金額
* `description (string)`: Cashtrayの説明文
* `account (AccountWithUser)`: 発行店舗のウォレット
* `expires_at (string)`: Cashtrayの失効日時
* `canceled_at (string)`: Cashtrayの無効化日時。NULLの場合は無効化されていません
* `token (string)`: CashtrayのQRコードを解析したときに出てくるURL

`account`は [AccountWithUser](#account-with-user) オブジェクトを返します。

<a name="cashtray-with-result"></a>
## CashtrayWithResult
* `id (string)`: CashtrayのID
* `amount (number)`: 取引金額
* `description (string)`: Cashtrayの説明文(アプリ上で取引の説明文として表示される)
* `account (AccountWithUser)`: 発行店舗のウォレット
* `expires_at (string)`: Cashtrayの失効日時
* `canceled_at (string)`: Cashtrayの無効化日時。NULLの場合は無効化されていません
* `token (string)`: CashtrayのQRコードを解析したときに出てくるURL
* `attempt (CashtrayAttempt)`: Cashtray読み取り結果
* `transaction (Transaction)`: 取引結果

`account`は [AccountWithUser](#account-with-user) オブジェクトを返します。

`attempt`は [CashtrayAttempt](#cashtray-attempt) オブジェクトを返します。

`transaction`は [Transaction](#transaction) オブジェクトを返します。

<a name="user"></a>
## User
* `id (string)`: ユーザー (または店舗) ID
* `name (string)`: ユーザー (または店舗) 名
* `is_merchant (boolean)`: 店舗ユーザーかどうか

<a name="organization"></a>
## Organization
* `code (string)`: 組織コード
* `name (string)`: 組織名

<a name="transaction-detail"></a>
## TransactionDetail
* `id (string)`: 取引ID
* `type (string)`: 取引種別
* `is_modified (boolean)`: 返金された取引かどうか
* `sender (User)`: 送金者情報
* `sender_account (Account)`: 送金ウォレット情報
* `receiver (User)`: 受取者情報
* `receiver_account (Account)`: 受取ウォレット情報
* `amount (number)`: 取引総額 (マネー額 + ポイント額)
* `money_amount (number)`: 取引マネー額
* `point_amount (number)`: 取引ポイント額(キャンペーン付与ポイント合算)
* `raw_point_amount (number)`: 取引ポイント額
* `campaign_point_amount (number)`: キャンペーンによるポイント付与額
* `done_at (string)`: 取引日時
* `description (string)`: 取引説明文
* `transfers (Transfer[])`: 

`receiver`と`sender`は [User](#user) オブジェクトを返します。

`receiver_account`と`sender_account`は [Account](#account) オブジェクトを返します。

`transfers`は [Transfer](#transfer) オブジェクトの配列を返します。

<a name="shop-with-accounts"></a>
## ShopWithAccounts
* `id (string)`: 店舗ID
* `name (string)`: 店舗名
* `organization_code (string)`: 組織コード
* `status (string)`: 店舗の状態
* `postal_code (string)`: 店舗の郵便番号
* `address (string)`: 店舗の住所
* `tel (string)`: 店舗の電話番号
* `email (string)`: 店舗のメールアドレス
* `external_id (string)`: 店舗の外部ID
* `accounts (ShopAccount[])`: 

`accounts`は [ShopAccount](#shop-account) オブジェクトの配列を返します。

<a name="bulk-transaction"></a>
## BulkTransaction
* `id (string)`: 
* `request_id (string)`: リクエストID
* `name (string)`: バルク取引管理用の名前
* `description (string)`: バルク取引管理用の説明文
* `status (string)`: バルク取引の状態
* `error (string)`: バルク取引のエラー種別
* `error_lineno (number)`: バルク取引のエラーが発生した行番号
* `submitted_at (string)`: バルク取引が登録された日時
* `updated_at (string)`: バルク取引が更新された日時

<a name="external-transaction-detail"></a>
## ExternalTransactionDetail
* `id (string)`: ポケペイ外部取引ID
* `is_modified (boolean)`: 返金された取引かどうか
* `sender (User)`: 送金者情報
* `sender_account (Account)`: 送金ウォレット情報
* `receiver (User)`: 受取者情報
* `receiver_account (Account)`: 受取ウォレット情報
* `amount (number)`: 決済額
* `done_at (string)`: 取引日時
* `description (string)`: 取引説明文
* `transaction (TransactionDetail)`: 関連ポケペイ取引詳細

`receiver`と`sender`は [User](#user) オブジェクトを返します。

`receiver_account`と`sender_account`は [Account](#account) オブジェクトを返します。

`transaction`は [TransactionDetail](#transaction-detail) オブジェクトを返します。

<a name="paginated-private-money-organization-summaries"></a>
## PaginatedPrivateMoneyOrganizationSummaries
* `rows (PrivateMoneyOrganizationSummary[])`: 
* `count (number)`: 
* `pagination (Pagination)`: 

`rows`は [PrivateMoneyOrganizationSummary](#private-money-organization-summary) オブジェクトの配列を返します。

`pagination`は [Pagination](#pagination) オブジェクトを返します。

<a name="private-money-summary"></a>
## PrivateMoneySummary
* `topup_amount (number)`: 
* `refunded_topup_amount (number)`: 
* `payment_amount (number)`: 
* `refunded_payment_amount (number)`: 
* `added_point_amount (number)`: 
* `topup_point_amount (number)`: 
* `campaign_point_amount (number)`: 
* `refunded_added_point_amount (number)`: 
* `exchange_inflow_amount (number)`: 
* `exchange_outflow_amount (number)`: 
* `transaction_count (number)`: 

<a name="user-stats-operation"></a>
## UserStatsOperation
* `id (string)`: 集計処理ID
* `from (string)`: 集計期間の開始時刻
* `to (string)`: 集計期間の終了時刻
* `status (string)`: 集計処理の実行ステータス
* `error_reason (string)`: エラーとなった理由
* `done_at (string)`: 集計処理の完了時刻
* `file_url (string)`: 集計結果のCSVのダウンロードURL
* `requested_at (string)`: 集計リクエストを行った時刻

<a name="user-device"></a>
## UserDevice
* `id (string)`: デバイスID
* `user (User)`: デバイスを使用するユーザ
* `is_active (boolean)`: デバイスが有効か
* `metadata (string)`: デバイスのメタデータ

`user`は [User](#user) オブジェクトを返します。

<a name="bank-registering-info"></a>
## BankRegisteringInfo
* `redirect_url (string)`: 
* `paytree_customer_number (string)`: 

<a name="banks"></a>
## Banks
* `rows (Bank[])`: 
* `count (number)`: 

`rows`は [Bank](#bank) オブジェクトの配列を返します。

<a name="paginated-transaction"></a>
## PaginatedTransaction
* `rows (Transaction[])`: 
* `count (number)`: 
* `pagination (Pagination)`: 

`rows`は [Transaction](#transaction) オブジェクトの配列を返します。

`pagination`は [Pagination](#pagination) オブジェクトを返します。

<a name="paginated-transaction-v2"></a>
## PaginatedTransactionV2
* `rows (Transaction[])`: 
* `per_page (number)`: 
* `count (number)`: 
* `next_page_cursor_id (string)`: 
* `prev_page_cursor_id (string)`: 

`rows`は [Transaction](#transaction) オブジェクトの配列を返します。

<a name="paginated-transfers"></a>
## PaginatedTransfers
* `rows (Transfer[])`: 
* `count (number)`: 
* `pagination (Pagination)`: 

`rows`は [Transfer](#transfer) オブジェクトの配列を返します。

`pagination`は [Pagination](#pagination) オブジェクトを返します。

<a name="paginated-transfers-v2"></a>
## PaginatedTransfersV2
* `rows (Transfer[])`: 
* `per_page (number)`: 
* `count (number)`: 
* `next_page_cursor_id (string)`: 
* `prev_page_cursor_id (string)`: 

`rows`は [Transfer](#transfer) オブジェクトの配列を返します。

<a name="paginated-account-with-users"></a>
## PaginatedAccountWithUsers
* `rows (AccountWithUser[])`: 
* `count (number)`: 
* `pagination (Pagination)`: 

`rows`は [AccountWithUser](#account-with-user) オブジェクトの配列を返します。

`pagination`は [Pagination](#pagination) オブジェクトを返します。

<a name="paginated-account-details"></a>
## PaginatedAccountDetails
* `rows (AccountDetail[])`: 
* `count (number)`: 
* `pagination (Pagination)`: 

`rows`は [AccountDetail](#account-detail) オブジェクトの配列を返します。

`pagination`は [Pagination](#pagination) オブジェクトを返します。

<a name="paginated-account-balance"></a>
## PaginatedAccountBalance
* `rows (AccountBalance[])`: 
* `count (number)`: 
* `pagination (Pagination)`: 

`rows`は [AccountBalance](#account-balance) オブジェクトの配列を返します。

`pagination`は [Pagination](#pagination) オブジェクトを返します。

<a name="paginated-shops"></a>
## PaginatedShops
* `rows (ShopWithMetadata[])`: 
* `count (number)`: 
* `pagination (Pagination)`: 

`rows`は [ShopWithMetadata](#shop-with-metadata) オブジェクトの配列を返します。

`pagination`は [Pagination](#pagination) オブジェクトを返します。

<a name="paginated-bills"></a>
## PaginatedBills
* `rows (Bill[])`: 
* `count (number)`: 
* `pagination (Pagination)`: 

`rows`は [Bill](#bill) オブジェクトの配列を返します。

`pagination`は [Pagination](#pagination) オブジェクトを返します。

<a name="paginated-private-moneys"></a>
## PaginatedPrivateMoneys
* `rows (PrivateMoney[])`: 
* `count (number)`: 
* `pagination (Pagination)`: 

`rows`は [PrivateMoney](#private-money) オブジェクトの配列を返します。

`pagination`は [Pagination](#pagination) オブジェクトを返します。

<a name="campaign"></a>
## Campaign
* `id (string)`: キャンペーンID
* `name (string)`: キャペーン名
* `applicable_shops (User[])`: キャンペーン適用対象の店舗リスト
* `is_exclusive (boolean)`: キャンペーンの重複を許すかどうかのフラグ
* `starts_at (string)`: キャンペーン開始日時
* `ends_at (string)`: キャンペーン終了日時
* `point_expires_at (string)`: キャンペーンによって付与されるポイントの失効日時
* `point_expires_in_days (number)`: キャンペーンによって付与されるポイントの有効期限(相対指定、単位は日)
* `priority (number)`: キャンペーンの優先順位
* `description (string)`: キャンペーン説明文
* `bear_point_shop (User)`: ポイントを負担する店舗
* `private_money (PrivateMoney)`: キャンペーンを適用するマネー
* `dest_private_money (PrivateMoney)`: ポイントを付与するマネー
* `max_total_point_amount (number)`: 一人当たりの累計ポイント上限
* `point_calculation_rule (string)`: ポイント計算ルール (banklisp表記)
* `point_calculation_rule_object (string)`: ポイント計算ルール (JSON文字列による表記)
* `status (string)`: キャンペーンの現在の状態
* `budget_caps_amount (number)`: キャンペーンの予算上限額
* `budget_current_amount (number)`: キャンペーンの付与合計額
* `budget_current_time (string)`: キャンペーンの付与集計日時

`applicable-shops`は [User](#user) オブジェクトの配列を返します。

`bear_point_shop`は [User](#user) オブジェクトを返します。

`dest_private_money`と`private_money`は [PrivateMoney](#private-money) オブジェクトを返します。

<a name="paginated-campaigns"></a>
## PaginatedCampaigns
* `rows (Campaign[])`: 
* `count (number)`: 
* `pagination (Pagination)`: 

`rows`は [Campaign](#campaign) オブジェクトの配列を返します。

`pagination`は [Pagination](#pagination) オブジェクトを返します。

<a name="account-transfer-summary"></a>
## AccountTransferSummary
* `summaries (AccountTransferSummaryElement[])`: 

`summaries`は [AccountTransferSummaryElement](#account-transfer-summary-element) オブジェクトの配列を返します。

<a name="organization-worker-task-webhook"></a>
## OrganizationWorkerTaskWebhook
* `id (string)`: 
* `organization_code (string)`: 
* `task (string)`: 
* `url (string)`: 
* `content_type (string)`: 
* `is_active (boolean)`: 

<a name="paginated-organization-worker-task-webhook"></a>
## PaginatedOrganizationWorkerTaskWebhook
* `rows (OrganizationWorkerTaskWebhook[])`: 
* `count (number)`: 
* `pagination (Pagination)`: 

`rows`は [OrganizationWorkerTaskWebhook](#organization-worker-task-webhook) オブジェクトの配列を返します。

`pagination`は [Pagination](#pagination) オブジェクトを返します。

<a name="coupon-detail"></a>
## CouponDetail
* `id (string)`: クーポンID
* `name (string)`: クーポン名
* `issued_shop (User)`: クーポン発行店舗
* `description (string)`: クーポンの説明文
* `discount_amount (number)`: クーポンによる値引き額(絶対値指定)
* `discount_percentage (number)`: クーポンによる値引き率
* `discount_upper_limit (number)`: クーポンによる値引き上限(値引き率が指定された場合の値引き上限額)
* `starts_at (string)`: クーポンの利用可能期間(開始日時)
* `ends_at (string)`: クーポンの利用可能期間(終了日時)
* `display_starts_at (string)`: クーポンの掲載期間(開始日時)
* `display_ends_at (string)`: クーポンの掲載期間(終了日時)
* `usage_limit (number)`: ユーザごとの利用可能回数(NULLの場合は無制限)
* `min_amount (number)`: クーポン適用可能な最小取引額
* `is_shop_specified (boolean)`: 特定店舗限定のクーポンかどうか
* `is_hidden (boolean)`: クーポン一覧に掲載されるかどうか
* `is_public (boolean)`: アプリ配信なしで受け取れるかどうか
* `code (string)`: クーポン受け取りコード
* `is_disabled (boolean)`: 無効化フラグ
* `token (string)`: クーポンを特定するためのトークン
* `coupon_image (string)`: クーポン画像のURL
* `available_shops (User[])`: 利用可能店舗リスト
* `private_money (PrivateMoney)`: クーポンのマネー

`issued_shop`は [User](#user) オブジェクトを返します。

`available-shops`は [User](#user) オブジェクトの配列を返します。

`private_money`は [PrivateMoney](#private-money) オブジェクトを返します。

<a name="paginated-coupons"></a>
## PaginatedCoupons
* `rows (Coupon[])`: 
* `count (number)`: 
* `pagination (Pagination)`: 

`rows`は [Coupon](#coupon) オブジェクトの配列を返します。

`pagination`は [Pagination](#pagination) オブジェクトを返します。

<a name="paginated-organizations"></a>
## PaginatedOrganizations
* `rows (Organization[])`: 
* `count (number)`: 
* `pagination (Pagination)`: 

`rows`は [Organization](#organization) オブジェクトの配列を返します。

`pagination`は [Pagination](#pagination) オブジェクトを返します。

<a name="private-money"></a>
## PrivateMoney
* `id (string)`: マネーID
* `name (string)`: マネー名
* `unit (string)`: マネー単位 (例: 円)
* `is_exclusive (boolean)`: 会員制のマネーかどうか
* `description (string)`: マネー説明文
* `oneline_message (string)`: マネーの要約
* `organization (Organization)`: マネーを発行した組織
* `max_balance (number)`: ウォレットの上限金額
* `transfer_limit (number)`: マネーの取引上限額
* `money_topup_transfer_limit (number)`: マネーチャージ取引上限額
* `type (string)`: マネー種別 (自家型=own, 第三者型=third-party)
* `expiration_type (string)`: 有効期限種別 (チャージ日起算=static, 最終利用日起算=last-update, 最終チャージ日起算=last-topup-update)
* `enable_topup_by_member (boolean)`:  (deprecated)
* `display_money_and_point (string)`: 

`organization`は [Organization](#organization) オブジェクトを返します。

<a name="pagination"></a>
## Pagination
* `current (number)`: 
* `per_page (number)`: 
* `max_page (number)`: 
* `has_prev (boolean)`: 
* `has_next (boolean)`: 

<a name="transaction"></a>
## Transaction
* `id (string)`: 取引ID
* `type (string)`: 取引種別
* `is_modified (boolean)`: 返金された取引かどうか
* `sender (User)`: 送金者情報
* `sender_account (Account)`: 送金ウォレット情報
* `receiver (User)`: 受取者情報
* `receiver_account (Account)`: 受取ウォレット情報
* `amount (number)`: 取引総額 (マネー額 + ポイント額)
* `money_amount (number)`: 取引マネー額
* `point_amount (number)`: 取引ポイント額(キャンペーン付与ポイント合算)
* `raw_point_amount (number)`: 取引ポイント額
* `campaign_point_amount (number)`: キャンペーンによるポイント付与額
* `done_at (string)`: 取引日時
* `description (string)`: 取引説明文

`receiver`と`sender`は [User](#user) オブジェクトを返します。

`receiver_account`と`sender_account`は [Account](#account) オブジェクトを返します。

<a name="external-transaction"></a>
## ExternalTransaction
* `id (string)`: ポケペイ外部取引ID
* `is_modified (boolean)`: 返金された取引かどうか
* `sender (User)`: 送金者情報
* `sender_account (Account)`: 送金ウォレット情報
* `receiver (User)`: 受取者情報
* `receiver_account (Account)`: 受取ウォレット情報
* `amount (number)`: 決済額
* `done_at (string)`: 取引日時
* `description (string)`: 取引説明文

`receiver`と`sender`は [User](#user) オブジェクトを返します。

`receiver_account`と`sender_account`は [Account](#account) オブジェクトを返します。

<a name="cashtray-attempt"></a>
## CashtrayAttempt
* `account (AccountWithUser)`: エンドユーザーのウォレット
* `status_code (number)`: ステータスコード
* `error_type (string)`: エラー型
* `error_message (string)`: エラーメッセージ
* `created_at (string)`: Cashtray読み取り記録の作成日時

`account`は [AccountWithUser](#account-with-user) オブジェクトを返します。

<a name="account"></a>
## Account
* `id (string)`: ウォレットID
* `name (string)`: ウォレット名
* `is_suspended (boolean)`: ウォレットが凍結されているかどうか
* `status (string)`: 
* `private_money (PrivateMoney)`: 設定マネー情報

`private_money`は [PrivateMoney](#private-money) オブジェクトを返します。

<a name="transfer"></a>
## Transfer
* `id (string)`: 
* `sender_account (AccountWithoutPrivateMoneyDetail)`: 
* `receiver_account (AccountWithoutPrivateMoneyDetail)`: 
* `amount (number)`: 
* `money_amount (number)`: 
* `point_amount (number)`: 
* `done_at (string)`: 
* `type (string)`: 
* `description (string)`: 
* `transaction_id (string)`: 

`receiver_account`と`sender_account`は [AccountWithoutPrivateMoneyDetail](#account-without-private-money-detail) オブジェクトを返します。

<a name="shop-account"></a>
## ShopAccount
* `id (string)`: ウォレットID
* `name (string)`: ウォレット名
* `is_suspended (boolean)`: ウォレットが凍結されているかどうか
* `can_transfer_topup (boolean)`: チャージ可能かどうか
* `private_money (PrivateMoney)`: 設定マネー情報

`private_money`は [PrivateMoney](#private-money) オブジェクトを返します。

<a name="private-money-organization-summary"></a>
## PrivateMoneyOrganizationSummary
* `organization_code (string)`: 
* `topup (OrganizationSummary)`: 
* `payment (OrganizationSummary)`: 

`payment`と`topup`は [OrganizationSummary](#organization-summary) オブジェクトを返します。

<a name="bank"></a>
## Bank
* `id (string)`: 
* `private_money (PrivateMoney)`: 
* `bank_name (string)`: 
* `bank_code (string)`: 
* `branch_number (string)`: 
* `branch_name (string)`: 
* `deposit_type (string)`: 
* `masked_account_number (string)`: 
* `account_name (string)`: 

`private_money`は [PrivateMoney](#private-money) オブジェクトを返します。

<a name="account-balance"></a>
## AccountBalance
* `expires_at (string)`: 
* `money_amount (number)`: 
* `point_amount (number)`: 

<a name="shop-with-metadata"></a>
## ShopWithMetadata
* `id (string)`: 店舗ID
* `name (string)`: 店舗名
* `organization_code (string)`: 組織コード
* `status (string)`: 店舗の状態
* `postal_code (string)`: 店舗の郵便番号
* `address (string)`: 店舗の住所
* `tel (string)`: 店舗の電話番号
* `email (string)`: 店舗のメールアドレス
* `external_id (string)`: 店舗の外部ID

<a name="account-transfer-summary-element"></a>
## AccountTransferSummaryElement
* `transfer_type (string)`: 
* `money_amount (number)`: 
* `point_amount (number)`: 
* `count (number)`: 

<a name="coupon"></a>
## Coupon
* `id (string)`: クーポンID
* `name (string)`: クーポン名
* `issued_shop (User)`: クーポン発行店舗
* `description (string)`: クーポンの説明文
* `discount_amount (number)`: クーポンによる値引き額(絶対値指定)
* `discount_percentage (number)`: クーポンによる値引き率
* `discount_upper_limit (number)`: クーポンによる値引き上限(値引き率が指定された場合の値引き上限額)
* `starts_at (string)`: クーポンの利用可能期間(開始日時)
* `ends_at (string)`: クーポンの利用可能期間(終了日時)
* `display_starts_at (string)`: クーポンの掲載期間(開始日時)
* `display_ends_at (string)`: クーポンの掲載期間(終了日時)
* `usage_limit (number)`: ユーザごとの利用可能回数(NULLの場合は無制限)
* `min_amount (number)`: クーポン適用可能な最小取引額
* `is_shop_specified (boolean)`: 特定店舗限定のクーポンかどうか
* `is_hidden (boolean)`: クーポン一覧に掲載されるかどうか
* `is_public (boolean)`: アプリ配信なしで受け取れるかどうか
* `code (string)`: クーポン受け取りコード
* `is_disabled (boolean)`: 無効化フラグ
* `token (string)`: クーポンを特定するためのトークン

`issued_shop`は [User](#user) オブジェクトを返します。

<a name="account-without-private-money-detail"></a>
## AccountWithoutPrivateMoneyDetail
* `id (string)`: 
* `name (string)`: 
* `is_suspended (boolean)`: 
* `status (string)`: 
* `private_money_id (string)`: 
* `user (User)`: 

`user`は [User](#user) オブジェクトを返します。

<a name="organization-summary"></a>
## OrganizationSummary
* `count (number)`: 
* `money_amount (number)`: 
* `money_count (number)`: 
* `point_amount (number)`: 
* `raw_point_amount (number)`: 
* `campaign_point_amount (number)`: 
* `point_count (number)`: 
