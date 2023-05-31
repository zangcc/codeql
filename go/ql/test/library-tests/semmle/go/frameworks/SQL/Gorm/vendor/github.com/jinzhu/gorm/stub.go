// Code generated by depstubber. DO NOT EDIT.
// This is a simple stub for github.com/jinzhu/gorm, strictly for use in testing.

// See the LICENSE file for information about the licensing of the original library.
// Source: github.com/jinzhu/gorm (exports: DB; functions: )

// Package gorm is a stub of github.com/jinzhu/gorm, generated by depstubber.
package gorm

import (
	context "context"
	sql "database/sql"
	reflect "reflect"
	sync "sync"
	time "time"
)

type Association struct {
	Error error
}

func (_ *Association) Append(_ ...interface{}) *Association {
	return nil
}

func (_ *Association) Clear() *Association {
	return nil
}

func (_ *Association) Count() int {
	return 0
}

func (_ *Association) Delete(_ ...interface{}) *Association {
	return nil
}

func (_ *Association) Find(_ interface{}) *Association {
	return nil
}

func (_ *Association) Replace(_ ...interface{}) *Association {
	return nil
}

type Callback struct{}

func (_ *Callback) Create() *CallbackProcessor {
	return nil
}

func (_ *Callback) Delete() *CallbackProcessor {
	return nil
}

func (_ *Callback) Query() *CallbackProcessor {
	return nil
}

func (_ *Callback) RowQuery() *CallbackProcessor {
	return nil
}

func (_ *Callback) Update() *CallbackProcessor {
	return nil
}

type CallbackProcessor struct{}

func (_ *CallbackProcessor) After(_ string) *CallbackProcessor {
	return nil
}

func (_ *CallbackProcessor) Before(_ string) *CallbackProcessor {
	return nil
}

func (_ *CallbackProcessor) Get(_ string) func(*Scope) {
	return nil
}

func (_ *CallbackProcessor) Register(_ string, _ func(*Scope)) {}

func (_ *CallbackProcessor) Remove(_ string) {}

func (_ *CallbackProcessor) Replace(_ string, _ func(*Scope)) {}

type DB struct {
	RWMutex      sync.RWMutex
	Value        interface{}
	Error        error
	RowsAffected int64
}

func (_ *DB) AddError(_ error) error {
	return nil
}

func (_ *DB) AddForeignKey(_ string, _ string, _ string, _ string) *DB {
	return nil
}

func (_ *DB) AddIndex(_ string, _ ...string) *DB {
	return nil
}

func (_ *DB) AddUniqueIndex(_ string, _ ...string) *DB {
	return nil
}

func (_ *DB) Assign(_ ...interface{}) *DB {
	return nil
}

func (_ *DB) Association(_ string) *Association {
	return nil
}

func (_ *DB) Attrs(_ ...interface{}) *DB {
	return nil
}

func (_ *DB) AutoMigrate(_ ...interface{}) *DB {
	return nil
}

func (_ *DB) Begin() *DB {
	return nil
}

func (_ *DB) BeginTx(_ context.Context, _ *sql.TxOptions) *DB {
	return nil
}

func (_ *DB) BlockGlobalUpdate(_ bool) *DB {
	return nil
}

func (_ *DB) Callback() *Callback {
	return nil
}

func (_ *DB) Close() error {
	return nil
}

func (_ *DB) Commit() *DB {
	return nil
}

func (_ *DB) CommonDB() SQLCommon {
	return nil
}

func (_ *DB) Count(_ interface{}) *DB {
	return nil
}

func (_ *DB) Create(_ interface{}) *DB {
	return nil
}

func (_ *DB) CreateTable(_ ...interface{}) *DB {
	return nil
}

func (_ *DB) DB() *sql.DB {
	return nil
}

func (_ *DB) Debug() *DB {
	return nil
}

func (_ *DB) Delete(_ interface{}, _ ...interface{}) *DB {
	return nil
}

func (_ *DB) Dialect() Dialect {
	return nil
}

func (_ *DB) DropColumn(_ string) *DB {
	return nil
}

func (_ *DB) DropTable(_ ...interface{}) *DB {
	return nil
}

func (_ *DB) DropTableIfExists(_ ...interface{}) *DB {
	return nil
}

func (_ *DB) Exec(_ string, _ ...interface{}) *DB {
	return nil
}

func (_ *DB) Find(_ interface{}, _ ...interface{}) *DB {
	return nil
}

func (_ *DB) First(_ interface{}, _ ...interface{}) *DB {
	return nil
}

func (_ *DB) FirstOrCreate(_ interface{}, _ ...interface{}) *DB {
	return nil
}

func (_ *DB) FirstOrInit(_ interface{}, _ ...interface{}) *DB {
	return nil
}

func (_ *DB) Get(_ string) (interface{}, bool) {
	return nil, false
}

func (_ *DB) GetErrors() []error {
	return nil
}

func (_ *DB) Group(_ string) *DB {
	return nil
}

func (_ *DB) HasBlockGlobalUpdate() bool {
	return false
}

func (_ *DB) HasTable(_ interface{}) bool {
	return false
}

func (_ *DB) Having(_ interface{}, _ ...interface{}) *DB {
	return nil
}

func (_ *DB) InstantSet(_ string, _ interface{}) *DB {
	return nil
}

func (_ *DB) Joins(_ string, _ ...interface{}) *DB {
	return nil
}

func (_ *DB) Last(_ interface{}, _ ...interface{}) *DB {
	return nil
}

func (_ *DB) Limit(_ interface{}) *DB {
	return nil
}

func (_ *DB) Lock() {}

func (_ *DB) LogMode(_ bool) *DB {
	return nil
}

func (_ *DB) Model(_ interface{}) *DB {
	return nil
}

func (_ *DB) ModifyColumn(_ string, _ string) *DB {
	return nil
}

func (_ *DB) New() *DB {
	return nil
}

func (_ *DB) NewRecord(_ interface{}) bool {
	return false
}

func (_ *DB) NewScope(_ interface{}) *Scope {
	return nil
}

func (_ *DB) Not(_ interface{}, _ ...interface{}) *DB {
	return nil
}

func (_ *DB) Offset(_ interface{}) *DB {
	return nil
}

func (_ *DB) Omit(_ ...string) *DB {
	return nil
}

func (_ *DB) Or(_ interface{}, _ ...interface{}) *DB {
	return nil
}

func (_ *DB) Order(_ interface{}, _ ...bool) *DB {
	return nil
}

func (_ *DB) Pluck(_ string, _ interface{}) *DB {
	return nil
}

func (_ *DB) Preload(_ string, _ ...interface{}) *DB {
	return nil
}

func (_ *DB) Preloads(_ interface{}) *DB {
	return nil
}

func (_ *DB) QueryExpr() *SqlExpr {
	return nil
}

func (_ *DB) RLock() {}

func (_ *DB) RLocker() sync.Locker {
	return nil
}

func (_ *DB) RUnlock() {}

func (_ *DB) Raw(_ string, _ ...interface{}) *DB {
	return nil
}

func (_ *DB) RecordNotFound() bool {
	return false
}

func (_ *DB) Related(_ interface{}, _ ...string) *DB {
	return nil
}

func (_ *DB) RemoveForeignKey(_ string, _ string) *DB {
	return nil
}

func (_ *DB) RemoveIndex(_ string) *DB {
	return nil
}

func (_ *DB) Rollback() *DB {
	return nil
}

func (_ *DB) RollbackUnlessCommitted() *DB {
	return nil
}

func (_ *DB) Row() *sql.Row {
	return nil
}

func (_ *DB) Rows() (*sql.Rows, error) {
	return nil, nil
}

func (_ *DB) Save(_ interface{}) *DB {
	return nil
}

func (_ *DB) Scan(_ interface{}) *DB {
	return nil
}

func (_ *DB) ScanRows(_ *sql.Rows, _ interface{}) error {
	return nil
}

func (_ *DB) Scopes(_ ...func(*DB) *DB) *DB {
	return nil
}

func (_ *DB) Select(_ interface{}, _ ...interface{}) *DB {
	return nil
}

func (_ *DB) Set(_ string, _ interface{}) *DB {
	return nil
}

func (_ *DB) SetJoinTableHandler(_ interface{}, _ string, _ JoinTableHandlerInterface) {}

func (_ *DB) SetLogger(_ interface{}) {}

func (_ *DB) SetNowFuncOverride(_ func() time.Time) *DB {
	return nil
}

func (_ *DB) SingularTable(_ bool) {}

func (_ *DB) SubQuery() *SqlExpr {
	return nil
}

func (_ *DB) Table(_ string) *DB {
	return nil
}

func (_ *DB) Take(_ interface{}, _ ...interface{}) *DB {
	return nil
}

func (_ *DB) Transaction(_ func(*DB) error) error {
	return nil
}

func (_ *DB) Unlock() {}

func (_ *DB) Unscoped() *DB {
	return nil
}

func (_ *DB) Update(_ ...interface{}) *DB {
	return nil
}

func (_ *DB) UpdateColumn(_ ...interface{}) *DB {
	return nil
}

func (_ *DB) UpdateColumns(_ interface{}) *DB {
	return nil
}

func (_ *DB) Updates(_ interface{}, _ ...bool) *DB {
	return nil
}

func (_ *DB) Where(_ interface{}, _ ...interface{}) *DB {
	return nil
}

type Dialect interface {
	BindVar(_ int) string
	BuildKeyName(_ string, _ string, _ ...string) string
	CurrentDatabase() string
	DataTypeOf(_ *StructField) string
	DefaultValueStr() string
	GetName() string
	HasColumn(_ string, _ string) bool
	HasForeignKey(_ string, _ string) bool
	HasIndex(_ string, _ string) bool
	HasTable(_ string) bool
	LastInsertIDOutputInterstitial(_ string, _ string, _ []string) string
	LastInsertIDReturningSuffix(_ string, _ string) string
	LimitAndOffsetSQL(_ interface{}, _ interface{}) (string, error)
	ModifyColumn(_ string, _ string, _ string) error
	NormalizeIndexAndColumn(_ string, _ string) (string, string)
	Quote(_ string) string
	RemoveIndex(_ string, _ string) error
	SelectFromDummyTable() string
	SetDB(_ SQLCommon)
}

type Field struct {
	StructField *StructField
	IsBlank     bool
	Field       reflect.Value
}

func (_ Field) TagSettingsDelete(_ string) {}

func (_ Field) TagSettingsGet(_ string) (string, bool) {
	return "", false
}

func (_ Field) TagSettingsSet(_ string, _ string) {}

func (_ *Field) Set(_ interface{}) error {
	return nil
}

type JoinTableForeignKey struct {
	DBName            string
	AssociationDBName string
}

type JoinTableHandlerInterface interface {
	Add(_ JoinTableHandlerInterface, _ *DB, _ interface{}, _ interface{}) error
	Delete(_ JoinTableHandlerInterface, _ *DB, _ ...interface{}) error
	DestinationForeignKeys() []JoinTableForeignKey
	JoinWith(_ JoinTableHandlerInterface, _ *DB, _ interface{}) *DB
	Setup(_ *Relationship, _ string, _ reflect.Type, _ reflect.Type)
	SourceForeignKeys() []JoinTableForeignKey
	Table(_ *DB) string
}

type ModelStruct struct {
	PrimaryFields []*StructField
	StructFields  []*StructField
	ModelType     reflect.Type
}

func (_ *ModelStruct) TableName(_ *DB) string {
	return ""
}

type Relationship struct {
	Kind                         string
	PolymorphicType              string
	PolymorphicDBName            string
	PolymorphicValue             string
	ForeignFieldNames            []string
	ForeignDBNames               []string
	AssociationForeignFieldNames []string
	AssociationForeignDBNames    []string
	JoinTableHandler             JoinTableHandlerInterface
}

type SQLCommon interface {
	Exec(_ string, _ ...interface{}) (sql.Result, error)
	Prepare(_ string) (*sql.Stmt, error)
	Query(_ string, _ ...interface{}) (*sql.Rows, error)
	QueryRow(_ string, _ ...interface{}) *sql.Row
}

type Scope struct {
	Search  interface{}
	Value   interface{}
	SQL     string
	SQLVars []interface{}
}

func (_ *Scope) AddToVars(_ interface{}) string {
	return ""
}

func (_ *Scope) Begin() *Scope {
	return nil
}

func (_ *Scope) CallMethod(_ string) {}

func (_ *Scope) CombinedConditionSql() string {
	return ""
}

func (_ *Scope) CommitOrRollback() *Scope {
	return nil
}

func (_ *Scope) DB() *DB {
	return nil
}

func (_ *Scope) Dialect() Dialect {
	return nil
}

func (_ *Scope) Err(_ error) error {
	return nil
}

func (_ *Scope) Exec() *Scope {
	return nil
}

func (_ *Scope) FieldByName(_ string) (*Field, bool) {
	return nil, false
}

func (_ *Scope) Fields() []*Field {
	return nil
}

func (_ *Scope) Get(_ string) (interface{}, bool) {
	return nil, false
}

func (_ *Scope) GetModelStruct() *ModelStruct {
	return nil
}

func (_ *Scope) GetStructFields() []*StructField {
	return nil
}

func (_ *Scope) HasColumn(_ string) bool {
	return false
}

func (_ *Scope) HasError() bool {
	return false
}

func (_ *Scope) IndirectValue() reflect.Value {
	return reflect.Value{}
}

func (_ *Scope) InstanceGet(_ string) (interface{}, bool) {
	return nil, false
}

func (_ *Scope) InstanceID() string {
	return ""
}

func (_ *Scope) InstanceSet(_ string, _ interface{}) *Scope {
	return nil
}

func (_ *Scope) Log(_ ...interface{}) {}

func (_ *Scope) New(_ interface{}) *Scope {
	return nil
}

func (_ *Scope) NewDB() *DB {
	return nil
}

func (_ *Scope) OmitAttrs() []string {
	return nil
}

func (_ *Scope) PrimaryField() *Field {
	return nil
}

func (_ *Scope) PrimaryFields() []*Field {
	return nil
}

func (_ *Scope) PrimaryKey() string {
	return ""
}

func (_ *Scope) PrimaryKeyValue() interface{} {
	return nil
}

func (_ *Scope) PrimaryKeyZero() bool {
	return false
}

func (_ *Scope) Quote(_ string) string {
	return ""
}

func (_ *Scope) QuotedTableName() string {
	return ""
}

func (_ *Scope) Raw(_ string) *Scope {
	return nil
}

func (_ *Scope) SQLDB() SQLCommon {
	return nil
}

func (_ *Scope) SelectAttrs() []string {
	return nil
}

func (_ *Scope) Set(_ string, _ interface{}) *Scope {
	return nil
}

func (_ *Scope) SetColumn(_ interface{}, _ interface{}) error {
	return nil
}

func (_ *Scope) SkipLeft() {}

func (_ *Scope) TableName() string {
	return ""
}

type SqlExpr struct{}

type StructField struct {
	DBName          string
	Name            string
	Names           []string
	IsPrimaryKey    bool
	IsNormal        bool
	IsIgnored       bool
	IsScanner       bool
	HasDefaultValue bool
	Tag             reflect.StructTag
	TagSettings     map[string]string
	Struct          reflect.StructField
	IsForeignKey    bool
	Relationship    *Relationship
}

func (_ *StructField) TagSettingsDelete(_ string) {}

func (_ *StructField) TagSettingsGet(_ string) (string, bool) {
	return "", false
}

func (_ *StructField) TagSettingsSet(_ string, _ string) {}
