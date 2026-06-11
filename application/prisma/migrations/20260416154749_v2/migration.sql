/*
  Warnings:

  - You are about to drop the column `type` on the `Stats` table. All the data in the column will be lost.
  - Added the required column `stat_type_id` to the `Stats` table without a default value. This is not possible if the table is not empty.

*/
-- AlterTable
ALTER TABLE "Stats" DROP COLUMN "type",
ADD COLUMN     "stat_type_id" TEXT NOT NULL;

-- DropEnum
DROP TYPE "STAT_TYPE";

-- CreateTable
CREATE TABLE "StatDataType" (
    "id" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "unit" TEXT NOT NULL,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "StatDataType_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "StatType" (
    "id" TEXT NOT NULL,
    "name" TEXT NOT NULL,
    "data_type_id" TEXT NOT NULL,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "StatType_pkey" PRIMARY KEY ("id")
);

-- AddForeignKey
ALTER TABLE "StatType" ADD CONSTRAINT "StatType_data_type_id_fkey" FOREIGN KEY ("data_type_id") REFERENCES "StatDataType"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Stats" ADD CONSTRAINT "Stats_stat_type_id_fkey" FOREIGN KEY ("stat_type_id") REFERENCES "StatType"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
