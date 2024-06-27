# Responses
<a name="account-with-user"></a>
## AccountWithUser
* `id (str)`: 
* `name (str)`: 
* `is_suspended (bool)`: 
* `status (str)`: 
* `private_money (PrivateMoney)`: 
* `user (User)`: 

`private_money`は [PrivateMoney](#private-money) オブジェクトを返します。

`user`は [User](#user) オブジェクトを返します。

<a name="account-detail"></a>
## AccountDetail
* `id (str)`: 
* `name (str)`: 
* `is_suspended (bool)`: 
* `status (str)`: 
* `balance (float)`: 
* `money_balance (float)`: 
* `point_balance (float)`: 
* `point_debt (float)`: 
* `private_money (PrivateMoney)`: 
* `user (User)`: 
* `external_id (str)`: 

`private_money`は [PrivateMoney](#private-money) オブジェクトを返します。

`user`は [User](#user) オブジェクトを返します。

<a name="account-deleted"></a>
## AccountDeleted

<a name="bill"></a>
## Bill
* `id (str)`: 支払いQRコードのID
* `amount (float)`: 支払い額
* `max_amount (float)`: 支払い額を範囲指定した場合の上限
* `min_amount (float)`: 支払い額を範囲指定した場合の下限
* `description (str)`: 支払いQRコードの説明文(アプリ上で取引の説明文として表示される)
* `account (AccountWithUser)`: 支払いQRコード発行ウォレット
* `is_disabled (bool)`: 無効化されているかどうか
* `token (str)`: 支払いQRコードを解析したときに出てくるURL

`account`は [AccountWithUser](#account-with-user) オブジェクトを返します。

<a name="check"></a>
## Check
* `id (str)`: チャージQRコードのID
* `created_at (str)`: チャージQRコードの作成日時
* `amount (float)`: チャージマネー額 (deprecated)
* `money_amount (float)`: チャージマネー額
* `point_amount (float)`: チャージポイント額
* `description (str)`: チャージQRコードの説明文(アプリ上で取引の説明文として表示される)
* `user (User)`: 送金元ユーザ情報
* `is_onetime (bool)`: 使用回数が一回限りかどうか
* `is_disabled (bool)`: 無効化されているかどうか
* `expires_at (str)`: チャージQRコード自体の失効日時
* `last_used_at (str)`: 
* `private_money (PrivateMoney)`: 対象マネー情報
* `usage_limit (int)`: 一回限りでない場合の最大読み取り回数
* `usage_count (float)`: 一回限りでない場合の現在までに読み取られた回数
* `point_expires_at (str)`: ポイント有効期限(絶対日数指定)
* `point_expires_in_days (int)`: ポイント有効期限(相対日数指定)
* `token (str)`: チャージQRコードを解析したときに出てくるURL

`user`は [User](#user) オブジェクトを返します。

`private_money`は [PrivateMoney](#private-money) オブジェクトを返します。

<a name="paginated-checks"></a>
## PaginatedChecks
* `rows (list of Checks)`: 
* `count (int)`: 
* `pagination (Pagination)`: 

`rows`は [Check](#check) オブジェクトのリストを返します。

`pagination`は [Pagination](#pagination) オブジェクトを返します。

<a name="cpm-token"></a>
## CpmToken
* `cpm_token (str)`: 
* `account (AccountDetail)`: 
* `transaction (Transaction)`: 
* `event (ExternalTransaction)`: 
* `scopes (list of strs)`: 許可された取引種別
* `expires_at (str)`: CPMトークンの失効日時
* `metadata (str)`: エンドユーザー側メタデータ

`account`は [AccountDetail](#account-detail) オブジェクトを返します。

`transaction`は [Transaction](#transaction) オブジェクトを返します。

`event`は [ExternalTransaction](#external-transaction) オブジェクトを返します。

<a name="cashtray"></a>
## Cashtray
* `id (str)`: Cashtray自体のIDです。
* `amount (float)`: 取引金額
* `description (str)`: Cashtrayの説明文
* `account (AccountWithUser)`: 発行店舗のウォレット
* `expires_at (str)`: Cashtrayの失効日時
* `canceled_at (str)`: Cashtrayの無効化日時。NULLの場合は無効化されていません
* `token (str)`: CashtrayのQRコードを解析したときに出てくるURL

`account`は [AccountWithUser](#account-with-user) オブジェクトを返します。

<a name="cashtray-with-result"></a>
## CashtrayWithResult
* `id (str)`: CashtrayのID
* `amount (float)`: 取引金額
* `description (str)`: Cashtrayの説明文(アプリ上で取引の説明文として表示される)
* `account (AccountWithUser)`: 発行店舗のウォレット
* `expires_at (str)`: Cashtrayの失効日時
* `canceled_at (str)`: Cashtrayの無効化日時。NULLの場合は無効化されていません
* `token (str)`: CashtrayのQRコードを解析したときに出てくるURL
* `attempt (CashtrayAttempt)`: Cashtray読み取り結果
* `transaction (Transaction)`: 取引結果

`account`は [AccountWithUser](#account-with-user) オブジェクトを返します。

`attempt`は [CashtrayAttempt](#cashtray-attempt) オブジェクトを返します。

`transaction`は [Transaction](#transaction) オブジェクトを返します。

<a name="user"></a>
## User
* `id (str)`: ユーザー (または店舗) ID
* `name (str)`: ユーザー (または店舗) 名
* `is_merchant (bool)`: 店舗ユーザーかどうか

<a name="organization"></a>
## Organization
* `code (str)`: 組織コード
* `name (str)`: 組織名

<a name="transaction-detail"></a>
## TransactionDetail
* `id (str)`: 取引ID
* `type (str)`: 取引種別
* `is_modified (bool)`: 返金された取引かどうか
* `sender (User)`: 送金者情報
* `sender_account (Account)`: 送金ウォレット情報
* `receiver (User)`: 受取者情報
* `receiver_account (Account)`: 受取ウォレット情報
* `amount (float)`: 取引総額 (マネー額 + ポイント額)
* `money_amount (float)`: 取引マネー額
* `point_amount (float)`: 取引ポイント額(キャンペーン付与ポイント合算)
* `raw_point_amount (float)`: 取引ポイント額
* `campaign_point_amount (float)`: キャンペーンによるポイント付与額
* `done_at (str)`: 取引日時
* `description (str)`: 取引説明文
* `transfers (list of Transfers)`: 

`receiver`と`sender`は [User](#user) オブジェクトを返します。

`receiver_account`と`sender_account`は [Account](#account) オブジェクトを返します。

`transfers`は [Transfer](#transfer) オブジェクトのリストを返します。

<a name="shop-with-accounts"></a>
## ShopWithAccounts
* `id (str)`: 店舗ID
* `name (str)`: 店舗名
* `organization_code (str)`: 組織コード
* `status (str)`: 店舗の状態
* `postal_code (str)`: 店舗の郵便番号
* `address (str)`: 店舗の住所
* `tel (str)`: 店舗の電話番号
* `email (str)`: 店舗のメールアドレス
* `external_id (str)`: 店舗の外部ID
* `accounts (list of ShopAccounts)`: 

`accounts`は [ShopAccount](#shop-account) オブジェクトのリストを返します。

<a name="bulk-transaction"></a>
## BulkTransaction
* `id (str)`: 
* `request_id (str)`: リクエストID
* `name (str)`: バルク取引管理用の名前
* `description (str)`: バルク取引管理用の説明文
* `status (str)`: バルク取引の状態
* `error (str)`: バルク取引のエラー種別
* `error_lineno (int)`: バルク取引のエラーが発生した行番号
* `submitted_at (str)`: バルク取引が登録された日時
* `updated_at (str)`: バルク取引が更新された日時

<a name="paginated-bulk-transaction-job"></a>
## PaginatedBulkTransactionJob
* `rows (list of BulkTransactionJobs)`: 
* `count (int)`: 
* `pagination (Pagination)`: 

`rows`は [BulkTransactionJob](#bulk-transaction-job) オブジェクトのリストを返します。

`pagination`は [Pagination](#pagination) オブジェクトを返します。

<a name="external-transaction-detail"></a>
## ExternalTransactionDetail
* `id (str)`: ポケペイ外部取引ID
* `is_modified (bool)`: 返金された取引かどうか
* `sender (User)`: 送金者情報
* `sender_account (Account)`: 送金ウォレット情報
* `receiver (User)`: 受取者情報
* `receiver_account (Account)`: 受取ウォレット情報
* `amount (float)`: 決済額
* `done_at (str)`: 取引日時
* `description (str)`: 取引説明文
* `transaction (TransactionDetail)`: 関連ポケペイ取引詳細

`receiver`と`sender`は [User](#user) オブジェクトを返します。

`receiver_account`と`sender_account`は [Account](#account) オブジェクトを返します。

`transaction`は [TransactionDetail](#transaction-detail) オブジェクトを返します。

<a name="paginated-private-money-organization-summaries"></a>
## PaginatedPrivateMoneyOrganizationSummaries
* `rows (list of PrivateMoneyOrganizationSummaries)`: 
* `count (int)`: 
* `pagination (Pagination)`: 

`rows`は [PrivateMoneyOrganizationSummary](#private-money-organization-summary) オブジェクトのリストを返します。

`pagination`は [Pagination](#pagination) オブジェクトを返します。

<a name="private-money-summary"></a>
## PrivateMoneySummary
* `topup_amount (float)`: 
* `refunded_topup_amount (float)`: 
* `payment_amount (float)`: 
* `refunded_payment_amount (float)`: 
* `added_point_amount (float)`: 
* `topup_point_amount (float)`: 
* `campaign_point_amount (float)`: 
* `refunded_added_point_amount (float)`: 
* `exchange_inflow_amount (float)`: 
* `exchange_outflow_amount (float)`: 
* `transaction_count (int)`: 

<a name="user-stats-operation"></a>
## UserStatsOperation
* `id (str)`: 集計処理ID
* `from (str)`: 集計期間の開始時刻
* `to (str)`: 集計期間の終了時刻
* `status (str)`: 集計処理の実行ステータス
* `error_reason (str)`: エラーとなった理由
* `done_at (str)`: 集計処理の完了時刻
* `file_url (str)`: 集計結果のCSVのダウンロードURL
* `requested_at (str)`: 集計リクエストを行った時刻

<a name="user-device"></a>
## UserDevice
* `id (str)`: デバイスID
* `user (User)`: デバイスを使用するユーザ
* `is_active (bool)`: デバイスが有効か
* `metadata (str)`: デバイスのメタデータ

`user`は [User](#user) オブジェクトを返します。

<a name="bank-registering-info"></a>
## BankRegisteringInfo
* `redirect_url (str)`: 
* `paytree_customer_number (str)`: 

<a name="banks"></a>
## Banks
* `rows (list of Banks)`: 
* `count (int)`: 

`rows`は [Bank](#bank) オブジェクトのリストを返します。

<a name="paginated-transaction"></a>
## PaginatedTransaction
* `rows (list of Transactions)`: 
* `count (int)`: 
* `pagination (Pagination)`: 

`rows`は [Transaction](#transaction) オブジェクトのリストを返します。

`pagination`は [Pagination](#pagination) オブジェクトを返します。

<a name="paginated-transaction-v2"></a>
## PaginatedTransactionV2
* `rows (list of Transactions)`: 
* `per_page (int)`: 
* `count (int)`: 
* `next_page_cursor_id (str)`: 
* `prev_page_cursor_id (str)`: 

`rows`は [Transaction](#transaction) オブジェクトのリストを返します。

<a name="paginated-transfers"></a>
## PaginatedTransfers
* `rows (list of Transfers)`: 
* `count (int)`: 
* `pagination (Pagination)`: 

`rows`は [Transfer](#transfer) オブジェクトのリストを返します。

`pagination`は [Pagination](#pagination) オブジェクトを返します。

<a name="paginated-transfers-v2"></a>
## PaginatedTransfersV2
* `rows (list of Transfers)`: 
* `per_page (int)`: 
* `count (int)`: 
* `next_page_cursor_id (str)`: 
* `prev_page_cursor_id (str)`: 

`rows`は [Transfer](#transfer) オブジェクトのリストを返します。

<a name="paginated-account-with-users"></a>
## PaginatedAccountWithUsers
* `rows (list of AccountWithUsers)`: 
* `count (int)`: 
* `pagination (Pagination)`: 

`rows`は [AccountWithUser](#account-with-user) オブジェクトのリストを返します。

`pagination`は [Pagination](#pagination) オブジェクトを返します。

<a name="paginated-account-details"></a>
## PaginatedAccountDetails
* `rows (list of AccountDetails)`: 
* `count (int)`: 
* `pagination (Pagination)`: 

`rows`は [AccountDetail](#account-detail) オブジェクトのリストを返します。

`pagination`は [Pagination](#pagination) オブジェクトを返します。

<a name="paginated-account-balance"></a>
## PaginatedAccountBalance
* `rows (list of AccountBalances)`: 
* `count (int)`: 
* `pagination (Pagination)`: 

`rows`は [AccountBalance](#account-balance) オブジェクトのリストを返します。

`pagination`は [Pagination](#pagination) オブジェクトを返します。

<a name="paginated-shops"></a>
## PaginatedShops
* `rows (list of ShopWithMetadatas)`: 
* `count (int)`: 
* `pagination (Pagination)`: 

`rows`は [ShopWithMetadata](#shop-with-metadata) オブジェクトのリストを返します。

`pagination`は [Pagination](#pagination) オブジェクトを返します。

<a name="paginated-bills"></a>
## PaginatedBills
* `rows (list of Bills)`: 
* `count (int)`: 
* `pagination (Pagination)`: 

`rows`は [Bill](#bill) オブジェクトのリストを返します。

`pagination`は [Pagination](#pagination) オブジェクトを返します。

<a name="paginated-private-moneys"></a>
## PaginatedPrivateMoneys
* `rows (list of PrivateMoneys)`: 
* `count (int)`: 
* `pagination (Pagination)`: 

`rows`は [PrivateMoney](#private-money) オブジェクトのリストを返します。

`pagination`は [Pagination](#pagination) オブジェクトを返します。

<a name="campaign"></a>
## Campaign
* `id (str)`: キャンペーンID
* `name (str)`: キャペーン名
* `applicable_shops (list of Users)`: キャンペーン適用対象の店舗リスト
* `is_exclusive (bool)`: キャンペーンの重複を許すかどうかのフラグ
* `starts_at (str)`: キャンペーン開始日時
* `ends_at (str)`: キャンペーン終了日時
* `point_expires_at (str)`: キャンペーンによって付与されるポイントの失効日時
* `point_expires_in_days (int)`: キャンペーンによって付与されるポイントの有効期限(相対指定、単位は日)
* `priority (int)`: キャンペーンの優先順位
* `description (str)`: キャンペーン説明文
* `bear_point_shop (User)`: ポイントを負担する店舗
* `private_money (PrivateMoney)`: キャンペーンを適用するマネー
* `dest_private_money (PrivateMoney)`: ポイントを付与するマネー
* `max_total_point_amount (int)`: 一人当たりの累計ポイント上限
* `point_calculation_rule (str)`: ポイント計算ルール (banklisp表記)
* `point_calculation_rule_object (str)`: ポイント計算ルール (JSON文字列による表記)
* `status (str)`: キャンペーンの現在の状態
* `budget_caps_amount (int)`: キャンペーンの予算上限額
* `budget_current_amount (int)`: キャンペーンの付与合計額
* `budget_current_time (str)`: キャンペーンの付与集計日時

`applicable-shops`は [User](#user) オブジェクトのリストを返します。

`bear_point_shop`は [User](#user) オブジェクトを返します。

`dest_private_money`と`private_money`は [PrivateMoney](#private-money) オブジェクトを返します。

<a name="paginated-campaigns"></a>
## PaginatedCampaigns
* `rows (list of Campaigns)`: 
* `count (int)`: 
* `pagination (Pagination)`: 

`rows`は [Campaign](#campaign) オブジェクトのリストを返します。

`pagination`は [Pagination](#pagination) オブジェクトを返します。

<a name="account-transfer-summary"></a>
## AccountTransferSummary
* `summaries (list of AccountTransferSummaryElements)`: 

`summaries`は [AccountTransferSummaryElement](#account-transfer-summary-element) オブジェクトのリストを返します。

<a name="organization-worker-task-webhook"></a>
## OrganizationWorkerTaskWebhook
* `id (str)`: 
* `organization_code (str)`: 
* `task (str)`: 
* `url (str)`: 
* `content_type (str)`: 
* `is_active (bool)`: 

<a name="paginated-organization-worker-task-webhook"></a>
## PaginatedOrganizationWorkerTaskWebhook
* `rows (list of OrganizationWorkerTaskWebhooks)`: 
* `count (int)`: 
* `pagination (Pagination)`: 

`rows`は [OrganizationWorkerTaskWebhook](#organization-worker-task-webhook) オブジェクトのリストを返します。

`pagination`は [Pagination](#pagination) オブジェクトを返します。

<a name="coupon-detail"></a>
## CouponDetail
* `id (str)`: クーポンID
* `name (str)`: クーポン名
* `issued_shop (User)`: クーポン発行店舗
* `description (str)`: クーポンの説明文
* `discount_amount (int)`: クーポンによる値引き額(絶対値指定)
* `discount_percentage (float)`: クーポンによる値引き率
* `discount_upper_limit (int)`: クーポンによる値引き上限(値引き率が指定された場合の値引き上限額)
* `starts_at (str)`: クーポンの利用可能期間(開始日時)
* `ends_at (str)`: クーポンの利用可能期間(終了日時)
* `display_starts_at (str)`: クーポンの掲載期間(開始日時)
* `display_ends_at (str)`: クーポンの掲載期間(終了日時)
* `usage_limit (int)`: ユーザごとの利用可能回数(NULLの場合は無制限)
* `min_amount (int)`: クーポン適用可能な最小取引額
* `is_shop_specified (bool)`: 特定店舗限定のクーポンかどうか
* `is_hidden (bool)`: クーポン一覧に掲載されるかどうか
* `is_public (bool)`: アプリ配信なしで受け取れるかどうか
* `code (str)`: クーポン受け取りコード
* `is_disabled (bool)`: 無効化フラグ
* `token (str)`: クーポンを特定するためのトークン
* `coupon_image (str)`: クーポン画像のURL
* `available_shops (list of Users)`: 利用可能店舗リスト
* `private_money (PrivateMoney)`: クーポンのマネー

`issued_shop`は [User](#user) オブジェクトを返します。

`available-shops`は [User](#user) オブジェクトのリストを返します。

`private_money`は [PrivateMoney](#private-money) オブジェクトを返します。

<a name="paginated-coupons"></a>
## PaginatedCoupons
* `rows (list of Coupons)`: 
* `count (int)`: 
* `pagination (Pagination)`: 

`rows`は [Coupon](#coupon) オブジェクトのリストを返します。

`pagination`は [Pagination](#pagination) オブジェクトを返します。

<a name="paginated-organizations"></a>
## PaginatedOrganizations
* `rows (list of Organizations)`: 
* `count (int)`: 
* `pagination (Pagination)`: 

`rows`は [Organization](#organization) オブジェクトのリストを返します。

`pagination`は [Pagination](#pagination) オブジェクトを返します。

<a name="private-money"></a>
## PrivateMoney
* `id (str)`: マネーID
* `name (str)`: マネー名
* `unit (str)`: マネー単位 (例: 円)
* `is_exclusive (bool)`: 会員制のマネーかどうか
* `description (str)`: マネー説明文
* `oneline_message (str)`: マネーの要約
* `organization (Organization)`: マネーを発行した組織
* `max_balance (float)`: ウォレットの上限金額
* `transfer_limit (float)`: マネーの取引上限額
* `money_topup_transfer_limit (float)`: マネーチャージ取引上限額
* `type (str)`: マネー種別 (自家型=own, 第三者型=third-party)
* `expiration_type (str)`: 有効期限種別 (チャージ日起算=static, 最終利用日起算=last-update, 最終チャージ日起算=last-topup-update)
* `enable_topup_by_member (bool)`:  (deprecated)
* `display_money_and_point (str)`: 

`organization`は [Organization](#organization) オブジェクトを返します。

<a name="pagination"></a>
## Pagination
* `current (int)`: 
* `per_page (int)`: 
* `max_page (int)`: 
* `has_prev (bool)`: 
* `has_next (bool)`: 

<a name="transaction"></a>
## Transaction
* `id (str)`: 取引ID
* `type (str)`: 取引種別
* `is_modified (bool)`: 返金された取引かどうか
* `sender (User)`: 送金者情報
* `sender_account (Account)`: 送金ウォレット情報
* `receiver (User)`: 受取者情報
* `receiver_account (Account)`: 受取ウォレット情報
* `amount (float)`: 取引総額 (マネー額 + ポイント額)
* `money_amount (float)`: 取引マネー額
* `point_amount (float)`: 取引ポイント額(キャンペーン付与ポイント合算)
* `raw_point_amount (float)`: 取引ポイント額
* `campaign_point_amount (float)`: キャンペーンによるポイント付与額
* `done_at (str)`: 取引日時
* `description (str)`: 取引説明文

`receiver`と`sender`は [User](#user) オブジェクトを返します。

`receiver_account`と`sender_account`は [Account](#account) オブジェクトを返します。

<a name="external-transaction"></a>
## ExternalTransaction
* `id (str)`: ポケペイ外部取引ID
* `is_modified (bool)`: 返金された取引かどうか
* `sender (User)`: 送金者情報
* `sender_account (Account)`: 送金ウォレット情報
* `receiver (User)`: 受取者情報
* `receiver_account (Account)`: 受取ウォレット情報
* `amount (float)`: 決済額
* `done_at (str)`: 取引日時
* `description (str)`: 取引説明文

`receiver`と`sender`は [User](#user) オブジェクトを返します。

`receiver_account`と`sender_account`は [Account](#account) オブジェクトを返します。

<a name="cashtray-attempt"></a>
## CashtrayAttempt
* `account (AccountWithUser)`: エンドユーザーのウォレット
* `status_code (float)`: ステータスコード
* `error_type (str)`: エラー型
* `error_message (str)`: エラーメッセージ
* `created_at (str)`: Cashtray読み取り記録の作成日時

`account`は [AccountWithUser](#account-with-user) オブジェクトを返します。

<a name="account"></a>
## Account
* `id (str)`: ウォレットID
* `name (str)`: ウォレット名
* `is_suspended (bool)`: ウォレットが凍結されているかどうか
* `status (str)`: 
* `private_money (PrivateMoney)`: 設定マネー情報

`private_money`は [PrivateMoney](#private-money) オブジェクトを返します。

<a name="transfer"></a>
## Transfer
* `id (str)`: 
* `sender_account (AccountWithoutPrivateMoneyDetail)`: 
* `receiver_account (AccountWithoutPrivateMoneyDetail)`: 
* `amount (float)`: 
* `money_amount (float)`: 
* `point_amount (float)`: 
* `done_at (str)`: 
* `type (str)`: 
* `description (str)`: 
* `transaction_id (str)`: 

`receiver_account`と`sender_account`は [AccountWithoutPrivateMoneyDetail](#account-without-private-money-detail) オブジェクトを返します。

<a name="shop-account"></a>
## ShopAccount
* `id (str)`: ウォレットID
* `name (str)`: ウォレット名
* `is_suspended (bool)`: ウォレットが凍結されているかどうか
* `can_transfer_topup (bool)`: チャージ可能かどうか
* `private_money (PrivateMoney)`: 設定マネー情報

`private_money`は [PrivateMoney](#private-money) オブジェクトを返します。

<a name="bulk-transaction-job"></a>
## BulkTransactionJob
* `id (int)`: 
* `bulk_transaction (BulkTransaction)`: 
* `type (str)`: 取引種別
* `sender_account_id (str)`: 
* `receiver_account_id (str)`: 
* `money_amount (float)`: 
* `point_amount (float)`: 
* `description (str)`: バルク取引ジョブ管理用の説明文
* `bear_point_account_id (str)`: 
* `point_expires_at (str)`: ポイント有効期限
* `status (str)`: バルク取引ジョブの状態
* `error (str)`: バルク取引のエラー種別
* `lineno (int)`: バルク取引のエラーが発生した行番号
* `transaction_id (str)`: 
* `created_at (str)`: バルク取引ジョブが登録された日時
* `updated_at (str)`: バルク取引ジョブが更新された日時

`bulk_transaction`は [BulkTransaction](#bulk-transaction) オブジェクトを返します。

<a name="private-money-organization-summary"></a>
## PrivateMoneyOrganizationSummary
* `organization_code (str)`: 
* `topup (OrganizationSummary)`: 
* `payment (OrganizationSummary)`: 

`payment`と`topup`は [OrganizationSummary](#organization-summary) オブジェクトを返します。

<a name="bank"></a>
## Bank
* `id (str)`: 
* `private_money (PrivateMoney)`: 
* `bank_name (str)`: 
* `bank_code (str)`: 
* `branch_number (str)`: 
* `branch_name (str)`: 
* `deposit_type (str)`: 
* `masked_account_number (str)`: 
* `account_name (str)`: 

`private_money`は [PrivateMoney](#private-money) オブジェクトを返します。

<a name="account-balance"></a>
## AccountBalance
* `expires_at (str)`: 
* `money_amount (float)`: 
* `point_amount (float)`: 

<a name="shop-with-metadata"></a>
## ShopWithMetadata
* `id (str)`: 店舗ID
* `name (str)`: 店舗名
* `organization_code (str)`: 組織コード
* `status (str)`: 店舗の状態
* `postal_code (str)`: 店舗の郵便番号
* `address (str)`: 店舗の住所
* `tel (str)`: 店舗の電話番号
* `email (str)`: 店舗のメールアドレス
* `external_id (str)`: 店舗の外部ID

<a name="account-transfer-summary-element"></a>
## AccountTransferSummaryElement
* `transfer_type (str)`: 
* `money_amount (float)`: 
* `point_amount (float)`: 
* `count (float)`: 

<a name="coupon"></a>
## Coupon
* `id (str)`: クーポンID
* `name (str)`: クーポン名
* `issued_shop (User)`: クーポン発行店舗
* `description (str)`: クーポンの説明文
* `discount_amount (int)`: クーポンによる値引き額(絶対値指定)
* `discount_percentage (float)`: クーポンによる値引き率
* `discount_upper_limit (int)`: クーポンによる値引き上限(値引き率が指定された場合の値引き上限額)
* `starts_at (str)`: クーポンの利用可能期間(開始日時)
* `ends_at (str)`: クーポンの利用可能期間(終了日時)
* `display_starts_at (str)`: クーポンの掲載期間(開始日時)
* `display_ends_at (str)`: クーポンの掲載期間(終了日時)
* `usage_limit (int)`: ユーザごとの利用可能回数(NULLの場合は無制限)
* `min_amount (int)`: クーポン適用可能な最小取引額
* `is_shop_specified (bool)`: 特定店舗限定のクーポンかどうか
* `is_hidden (bool)`: クーポン一覧に掲載されるかどうか
* `is_public (bool)`: アプリ配信なしで受け取れるかどうか
* `code (str)`: クーポン受け取りコード
* `is_disabled (bool)`: 無効化フラグ
* `token (str)`: クーポンを特定するためのトークン

`issued_shop`は [User](#user) オブジェクトを返します。

<a name="account-without-private-money-detail"></a>
## AccountWithoutPrivateMoneyDetail
* `id (str)`: 
* `name (str)`: 
* `is_suspended (bool)`: 
* `status (str)`: 
* `private_money_id (str)`: 
* `user (User)`: 

`user`は [User](#user) オブジェクトを返します。

<a name="organization-summary"></a>
## OrganizationSummary
* `count (int)`: 
* `money_amount (float)`: 
* `money_count (int)`: 
* `point_amount (float)`: 
* `raw_point_amount (float)`: 
* `campaign_point_amount (float)`: 
* `point_count (int)`: 
