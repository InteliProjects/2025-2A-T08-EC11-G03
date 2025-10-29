-- CreateTable
CREATE TABLE "animal_metadata" (
    "id" SERIAL NOT NULL,
    "device_id" TEXT NOT NULL,

    CONSTRAINT "animal_metadata_pkey" PRIMARY KEY ("id")
);

-- CreateTable
CREATE TABLE "collar_statuses" (
    "id" SERIAL NOT NULL,
    "coleira_id" TEXT NOT NULL,
    "status" TEXT NOT NULL,
    "created_at" TIMESTAMP(3) NOT NULL DEFAULT CURRENT_TIMESTAMP,
    "updated_at" TIMESTAMP(3) NOT NULL,

    CONSTRAINT "collar_statuses_pkey" PRIMARY KEY ("id")
);

-- CreateIndex
CREATE UNIQUE INDEX "animal_metadata_device_id_key" ON "animal_metadata"("device_id");

-- CreateIndex
CREATE UNIQUE INDEX "collar_statuses_coleira_id_key" ON "collar_statuses"("coleira_id");
