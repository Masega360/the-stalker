-- DropForeignKey
ALTER TABLE "Stats" DROP CONSTRAINT "Stats_device_id_fkey";

-- AlterTable
ALTER TABLE "StatDataType" ALTER COLUMN "unit" DROP NOT NULL;

-- AlterTable
ALTER TABLE "Stats" ADD COLUMN     "snapshot_id" TEXT,
ALTER COLUMN "time" SET DEFAULT CURRENT_TIMESTAMP,
ALTER COLUMN "device_id" DROP NOT NULL;

-- CreateIndex
CREATE UNIQUE INDEX "StatDataType_name_key" ON "StatDataType"("name");

-- CreateIndex
CREATE UNIQUE INDEX "StatType_name_key" ON "StatType"("name");

-- CreateIndex
CREATE INDEX "Stats_snapshot_id_idx" ON "Stats"("snapshot_id");

-- CreateIndex
CREATE INDEX "Stats_stat_type_id_idx" ON "Stats"("stat_type_id");

-- AddForeignKey
ALTER TABLE "Stats" ADD CONSTRAINT "Stats_device_id_fkey" FOREIGN KEY ("device_id") REFERENCES "Device"("id") ON DELETE SET NULL ON UPDATE CASCADE;
