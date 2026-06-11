-- CreateEnum
CREATE TYPE "CONDITION" AS ENUM ('GT', 'LT', 'EQ');

-- CreateTable
CREATE TABLE "Rule" (
    "id" TEXT NOT NULL,
    "sensor_device_id" TEXT NOT NULL,
    "condition" "CONDITION" NOT NULL,
    "comparator" DOUBLE PRECISION NOT NULL,
    "actuator_device_id" TEXT NOT NULL,
    "stat_type_id" TEXT NOT NULL,
    "stat_data_type_id" TEXT NOT NULL,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "Rule_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE INDEX "Rule_sensor_device_id_idx" ON "Rule"("sensor_device_id");

-- CreateIndex
CREATE INDEX "Rule_actuator_device_id_idx" ON "Rule"("actuator_device_id");

-- CreateIndex
CREATE INDEX "Rule_stat_type_id_idx" ON "Rule"("stat_type_id");

-- CreateIndex
CREATE INDEX "Rule_stat_data_type_id_idx" ON "Rule"("stat_data_type_id");

-- AddForeignKey
ALTER TABLE "Rule" ADD CONSTRAINT "Rule_sensor_device_id_fkey" FOREIGN KEY ("sensor_device_id") REFERENCES "Device"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Rule" ADD CONSTRAINT "Rule_actuator_device_id_fkey" FOREIGN KEY ("actuator_device_id") REFERENCES "Device"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Rule" ADD CONSTRAINT "Rule_stat_type_id_fkey" FOREIGN KEY ("stat_type_id") REFERENCES "StatType"("id") ON DELETE RESTRICT ON UPDATE CASCADE;

-- AddForeignKey
ALTER TABLE "Rule" ADD CONSTRAINT "Rule_stat_data_type_id_fkey" FOREIGN KEY ("stat_data_type_id") REFERENCES "StatDataType"("id") ON DELETE RESTRICT ON UPDATE CASCADE;
